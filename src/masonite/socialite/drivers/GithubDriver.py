import json

from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class GithubDriver(BaseDriver):
    def get_default_scopes(self):
        return ["user:email"]

    def get_auth_url(self):
        return "https://github.com/login/oauth/authorize"

    def get_token_url(self):
        return "https://github.com/login/oauth/access_token"

    def get_user_url(self):
        return "https://api.github.com/user"

    def get_request_options(self, token):
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
        return {
            "headers": {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }
        }

    def user(self):
        # TODO: session is not persisted ... ?
        # if self.has_invalid_state():
        #     raise Exception("Invalid state")
        user_data, token = super().user()
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["id"],
                    "nickname": user_data["login"],
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
                    "nickname": user_data["login"],
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "avatar": user_data["avatar_url"],
                }
            )
        )
        return user
