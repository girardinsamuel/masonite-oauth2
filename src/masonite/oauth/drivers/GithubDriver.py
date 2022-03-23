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

    def get_email_url(self):
        return "https://api.github.com/user/emails"

    def get_request_options(self, token):
        # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current-version
        return {
            "headers": {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            }
        }

    def get_email_by_token(self, token):
        email = ""
        if self.has_scope("user:email"):
            emails_data = super().get_email_by_token(token)
            for email_data in emails_data:
                if email_data["primary"] and email_data["verified"]:
                    email = email_data["email"]
                    break
        return email

    def map_user_data(self, data):
        return OAuthUser().build(
                {
                    "id": data["id"],
                    "nickname": data["login"],
                    "name": data["name"],
                    "email": data["email"],
                    "avatar": data["avatar_url"],
                }
            )
