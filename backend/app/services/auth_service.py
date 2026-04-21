from app.schemas.auth import TokenResponse, UserPublic


class AuthService:
    @staticmethod
    def build_token_response(user_id: int, name: str, email: str) -> TokenResponse:
        return TokenResponse(
            access_token="not-a-real-token",
            user=UserPublic(
                id=user_id,
                name=name,
                email=email,
            ),
        )
