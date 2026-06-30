package hub

import (
	"sync"

	"github.com/gorilla/websocket"
)

type Hub struct {
	rooms map[int]map[*websocket.Conn]struct{} // conversationID -> conn struct para no ocupar memoria
	mu sync.RWMutex
}

func (h *Hub) Register(conversationID int, conn *websocket.Conn) {
	h.mu.Lock()
	defer h.mu.Unlock()
	if _, ok := h.rooms[conversationID]; !ok {
		h.rooms[conversationID] = make(map[*websocket.Conn]struct{})
	}
	h.rooms[conversationID][conn] = struct{}{}
}

func (h *Hub) Unregister(conversationID int, conn *websocket.Conn) {
	h.mu.Lock()
	defer h.mu.Unlock()
	delete(h.rooms[conversationID], conn)
	if len(h.rooms[conversationID]) == 0 {
		delete(h.rooms, conversationID)
	}
}

func (h *Hub) Broadcast(conversationID int, message any) {
	h.mu.Lock()
	defer h.mu.Unlock()
}