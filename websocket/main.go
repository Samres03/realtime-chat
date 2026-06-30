package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"strconv"

	"github.com/Samres03/realtime-chat/websocket/types"
	"github.com/golang-jwt/jwt/v5"
	"github.com/gorilla/websocket"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/joho/godotenv"
)

type Server struct {
	env               types.Env
	pool              *pgxpool.Pool
	websocketUpgrader websocket.Upgrader
}

func (s *Server) wsHandler(w http.ResponseWriter, r *http.Request) {
	conversationID, err := strconv.Atoi(r.PathValue("conversation_id"))
	if err != nil {
		http.Error(w, "Invalid conversation ID", http.StatusBadRequest)
		return
	}

	token := r.URL.Query().Get("token")
	if token == "" {
		http.Error(w, "Token is required", http.StatusUnauthorized)
		return
	}

	conn, err := s.websocketUpgrader.Upgrade(w, r, nil)
	if err != nil {
		http.Error(w, "Failed to upgrade to WebSocket", http.StatusInternalServerError)
		return
	}

	defer func() {
		_ = conn.Close()
	}()

	userID, err := validateToken(s.env, token)
	if err != nil {
		_ = conn.WriteJSON(map[string]any{
			"type":    "error",
			"message": "Invalid token",
		})
		return
	}

	if !s.isConversationMember(context.Background(), userID, conversationID) {
		_ = conn.WriteJSON(map[string]any{
			"type":    "error",
			"message": "You are not a member of this conversation",
		})
		return
	}
	_ = conn.WriteJSON(map[string]any{
		"type":            "connected",
		"conversation_id": conversationID,
	})

	for {
		if _, _, err := conn.ReadMessage(); err != nil {
			break
		}
	}
}

func (s *Server) loadEnv() {
	secretKey := os.Getenv("JWT_SECRET_KEY")
	algorithm := os.Getenv("JWT_ALGORITHM")
	expireMinutes, err := strconv.Atoi(os.Getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES"))

	url := os.Getenv("DATABASE_URL")

	if err != nil {
		log.Fatal("Error converting JWT_ACCESS_TOKEN_EXPIRE_MINUTES to int")
	}

	s.env = types.Env{
		Jwt: types.EnvJwt{
			SecretKey:                secretKey,
			Algorithm:                algorithm,
			AccessTokenExpireMinutes: expireMinutes,
		},
		Db: types.EnvDb{
			Url: url,
		},
	}
}

func (s *Server) initDB(ctx context.Context) error {
	var err error
	s.pool, err = pgxpool.New(ctx, s.env.Db.Url)
	return err
}

func (s *Server) isConversationMember(ctx context.Context, userID int, conversationID int) bool {
	query := `
		SELECT EXISTS (
			SELECT 1 FROM conversation_members
			WHERE user_id = $1 AND conversation_id = $2
		)
	`
	var exists bool
	err := s.pool.QueryRow(ctx, query, userID, conversationID).Scan(&exists)
	if err != nil {
		return false
	}
	return exists
}

func validateToken(env types.Env, token string) (int, error) {
	parsedToken, err := jwt.Parse(token, func(t *jwt.Token) (any, error) {
		if t.Method.Alg() != env.Jwt.Algorithm {
			return nil, jwt.ErrTokenUnverifiable
		}
		return []byte(env.Jwt.SecretKey), nil
	}, jwt.WithValidMethods([]string{env.Jwt.Algorithm}))
	if err != nil || !parsedToken.Valid {
		return 0, err
	}
	claims, ok := parsedToken.Claims.(jwt.MapClaims)
	if !ok {
		return 0, jwt.ErrTokenInvalidClaims
	}
	sub, _ := claims["sub"].(string)
	userID, err := strconv.Atoi(sub)
	if err != nil {
		return 0, err
	}
	return userID, nil
}

func main() {
	if err := godotenv.Load(); err != nil {
		log.Fatal("Error loading .env file")
	}
	s := Server{
		websocketUpgrader: websocket.Upgrader{
			CheckOrigin: func(r *http.Request) bool { return true },
		},
	}
	s.loadEnv()
	if err := s.initDB(context.Background()); err != nil {
		log.Fatal("Error initializing database", err)
	}
	http.HandleFunc("/ws/conversation/{conversation_id}", s.wsHandler)
	log.Println("Server started on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
