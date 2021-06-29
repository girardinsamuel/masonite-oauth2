import json

from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class GitlabDriver(BaseDriver):
    def get_auth_url(self):
        return "https://gitlab.com/oauth/authorize"

    def get_token_url(self):
        return "https://gitlab.com/oauth/token"

    def user(self):
        # TODO: session is not persisted ... ?
        # if self.has_invalid_state():
        #     raise Exception("Invalid state")

        client, token = self.get_token()
        response = client.get("https://gitlab.com/api/v3/user")  # here client is authenticated
        user_data = json.loads(response.content.decode("utf-8"))
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
