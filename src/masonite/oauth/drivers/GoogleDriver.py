import requests

from .BaseDriver import BaseDriver


class GoogleDriver(BaseDriver):
    scope_separator = " "

    def get_default_scopes(self):
        return ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]

    def get_auth_url(self):
        return "https://accounts.google.com/o/oauth2/auth"

    def get_token_url(self):
        return "https://www.googleapis.com/oauth2/v4/token"

    def get_user_url(self):
        return "https://www.googleapis.com/oauth2/v3/userinfo"

    def get_request_options(self, token):
        return {
            "headers": {"Authorization": f"Bearer {token}", "Accept": "application/json"},
        }

    def get_token_fields(self, code):
        fields = super().get_token_fields(code)
        fields.update({
            "access_type": "offline",
            "include_granted_scopes": "true",
            "prompt": "consent"
        })
        return fields

    def map_user_data(self, data):
        return {
            "id": data.get("sub", ""),
            "nickname": data.get("nickname", ""),
            "name": data.get("name", ""),
            "email": data.get("email", ""),
            "avatar": data.get("picture", ""),
        }

    def revoke(self, token):
        # https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#oauth-2.0-endpoints_6
        response = requests.post(
            f"https://oauth2.googleapis.com/revoke?token={token}",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status_code == 200:
            return True
        else:
            return False
