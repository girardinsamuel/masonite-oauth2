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

    def get_email_url(self):
        return "https://api.bitbucket.org/2.0/user/emails"

    def get_request_options(self, token):
        return {"headers": {"Authorization": f"Bearer {token}"}}

    def user(self):
        user_data, token = super().user()
        email = self.get_email_by_token(token)
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["uuid"],
                    "nickname": user_data["username"],
                    "name": user_data["display_name"],
                    "email": user_data.get("email", "") or email,
                    "avatar": user_data["links"]["avatar"]["href"],
                }
            )
        )
        return user

    def get_email_by_token(self, token):
        email = ""
        if self.has_scope("email"):
            emails_data = super().get_email_by_token(token)
            for email_data in emails_data.get("values", []):
                if (
                    email_data["is_primary"]
                    and email_data["is_confirmed"]
                    and email_data["type"] == "email"
                ):
                    email = email_data["email"]
        return email

    def user_from_token(self, token):
        user_data = super().user_from_token(token)
        # fetch email if possible
        email = self.get_email_by_token(token)
        user = (
            OAuthUser()
            .set_token(token)
            .build(
                {
                    "id": user_data["uuid"],
                    "nickname": user_data["username"],
                    "name": user_data["display_name"],
                    "email": user_data.get("email", "") or email,
                    "avatar": user_data["links"]["avatar"]["href"],
                }
            )
        )
        return user
