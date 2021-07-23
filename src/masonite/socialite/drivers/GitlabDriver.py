import json

from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class GitlabDriver(BaseDriver):
    def get_default_scopes(self):
        return ["read_user"]

    def get_auth_url(self):
        return "https://gitlab.com/oauth/authorize"

    def get_token_url(self):
        return "https://gitlab.com/oauth/token"

    def get_user_url(self):
        return "https://gitlab.com/api/v4/user"

    def get_request_options(self, token):
        return {"headers": {"Authorization": f"Bearer {token}"}}

    def user(self):
        user_data, token = super().user()
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["id"],
                    "nickname": user_data["username"],
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "avatar": user_data["avatar_url"],
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
                    "id": user_data["id"],
                    "nickname": user_data["username"],
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "avatar": user_data["avatar_url"],
                }
            )
        )
        return user
