from .BaseDriver import BaseDriver


class GitlabDriver(BaseDriver):
    def get_default_scopes(self):
        return ["read_user"]

    def get_auth_url(self):
        return "https://gitlab.com/oauth/authorize"

    def get_token_url(self):
        return "https://gitlab.com/oauth/token"

    def get_email_url(self):
        return ""

    def get_user_url(self):
        return "https://gitlab.com/api/v4/user"

    def get_request_options(self, token):
        return {"headers": {"Authorization": f"Bearer {token}"}}

    def map_user_data(self, data):
        return {
            "id": data["id"],
            "nickname": data["username"],
            "name": data["name"],
            "email": data["email"],
            "avatar": data["avatar_url"],
        }

    def revoke(self, token):
        # https://docs.gitlab.com/ee/api/oauth2.html#revoke-a-token
        response = self.perform_basic_request(
            "post",
            "https://gitlab.com/oauth/revoke",
            json={"token": token},
            headers={"Accept": "application/json"},
        )
        if response.status_code == 200:
            return True
        else:
            return False
