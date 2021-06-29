import json

from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class GithubDriver(BaseDriver):
    def get_auth_url(self):
        return "https://github.com/login/oauth/authorize"

    def get_token_url(self):
        return "https://github.com/login/oauth/access_token"

    def redirect(self):
        client = self.get_client()
        authorization_url, state = client.authorization_url(self.get_auth_url())
        self.application.make("session").set("state", state)
        return self.application.make("response").redirect(location=authorization_url)

    def user(self):
        # TODO: session is not persisted ... ?
        # if self.has_invalid_state():
        #     raise Exception("Invalid state")

        request = self.application.make("request")
        code = request.input("code")
        client = self.get_client()
        response = client.fetch_token(
            self.get_token_url(),
            client_secret=self.options.get("client_secret"),
            code=code,
        )
        token = response.get("access_token")
        # token_type = response.get("token_type")
        # scope = response.get("scope")
        # response = client.get(
        #     "https://api.github.com/user", headers={"Authorization": f"token {token}"}
        # )
        response = client.get("https://api.github.com/user")  # here client is authenticated
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
