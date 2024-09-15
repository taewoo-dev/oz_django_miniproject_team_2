from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class TokenService:
    @staticmethod
    def generate_jwt_token(user: User) -> tuple[str, str]:
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token  # type: ignore
        return str(access), str(refresh)

    @staticmethod
    def blacklist_refresh_token(refresh_token: str) -> None:
        token = RefreshToken(refresh_token)  # type: ignore
        token.blacklist()
