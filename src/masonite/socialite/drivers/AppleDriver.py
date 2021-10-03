from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class AppleDriver(BaseDriver):
    def get_default_scopes(self):
        return ["name", "email"]

    def get_auth_url(self):
        return "https://appleid.apple.com/auth/authorize"

    def get_token_url(self):
        return "https://appleid.apple.com/auth/token"

    def user(self):
        user_data, token = super().user()
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["sub"],
                    "nickname": user_data["nickname"],
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "avatar": user_data["picture"],
                }
            )
        )
        return user

    def user_from_token(self, token):
        user_data = super().user_from_token(token)
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["sub"],
                    "nickname": user_data["nickname"],
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "avatar": user_data["picture"],
                }
            )
        )
        return user
