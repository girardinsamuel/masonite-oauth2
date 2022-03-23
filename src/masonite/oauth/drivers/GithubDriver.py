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
        return {
            "id": data["id"],
            "nickname": data["login"],
            "name": data["name"],
            "email": data["email"],
            "avatar": data["avatar_url"],
        }

    def revoke(self, token):
        # https://docs.github.com/en/rest/reference/apps#delete-an-app-token"
        response = self.perform_basic_request(
            "delete",
            f"https://api.github.com/applications/{self.options.get('client_id')}/grant",
            json={"access_token": token},
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        if response.status_code == 204:
            return True
        else:
            return False

    def user(self) -> "OAuthUser":
        """
        GitHub Oauth2 mechanism does not provide refresh token info from OAuth flow, a subsequent
        request needs to be done.
        https://docs.github.com/en/rest/reference/apps#check-a-token
        """

        if self.has_invalid_state():
            raise Exception("Invalid state")
        data = self.get_token()
        token = data.get("access_token")
        user = self.user_from_token(token)

        response = self.perform_basic_request(
            "post",
            f"https://api.github.com/applications/{self.options.get('client_id')}/token",
            json={"access_token": token},
            headers={"Accept": "application/vnd.github.v3+json"},
        )
        full_data = response.json()
        user.set_expires_in(full_data.get("expires_at"))
        return user
