from .BaseDriver import BaseDriver
from ..OAuthUser import OAuthUser


class BitbucketDriver(BaseDriver):
    def get_default_scopes(self):
        # https://developer.atlassian.com/cloud/bitbucket/bitbucket-cloud-rest-api-scopes/
        return ["email"]

    def get_auth_url(self):
        return "https://bitbucket.org/site/oauth2/authorize"

    def get_token_url(self):
        return "https://bitbucket.org/site/oauth2/access_token"

    def get_user_url(self):
        return "https://api.bitbucket.org/2.0/user"

    def get_request_options(self, token):
        return {"headers": {f"Authorization: Bearer {token}"}}

    def user(self):
        user_data, token = super().user()
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["uuid"],
                    "nickname": user_data["username"],
                    "name": user_data["display_name"],
                    "email": user_data.get("email", ""),
                    "avatar": user_data["links"]["avatar"]["href"],
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
                    "id": user_data["uuid"],
                    "nickname": user_data["username"],
                    "name": user_data["display_name"],
                    "email": user_data.get("email", ""),
                    "avatar": user_data["links"]["avatar"]["href"],
                }
            )
        )
        return user
