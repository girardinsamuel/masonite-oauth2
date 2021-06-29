import json

from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class GithubDriver(BaseDriver):
    def get_auth_url(self):
        return "https://github.com/login/oauth/authorize"

    def get_token_url(self):
        return "https://github.com/login/oauth/access_token"

    def get_user_url(self):
        return "https://api.github.com/user"

    def user(self):
        # TODO: session is not persisted ... ?
        # if self.has_invalid_state():
        #     raise Exception("Invalid state")

        client, token = self.get_token()
        response = client.get(self.get_user_url())  # here client is authenticated
        user_data = json.loads(response.content.decode("utf-8"))
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
