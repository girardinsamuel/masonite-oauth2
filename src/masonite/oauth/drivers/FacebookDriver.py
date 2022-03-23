from .BaseDriver import BaseDriver


class FacebookDriver(BaseDriver):
    def get_default_scopes(self):
        return ["email"]

    def get_auth_url(self):
        return "https://www.facebook.com/dialog/oauth"

    def get_token_url(self):
        return "https://graph.facebook.com/oauth/access_token"

    def get_user_url(self):
        return "https://graph.facebook.com/me?"

    def get_request_options(self, token):
        return {
            "headers": {"Authorization": f"Bearer {token}", "Accept": "application/json"},
            "query": {"prettyPrint": "false"},
        }

    def map_user_data(self, data):
        return {
            "id": data["sub"],
            "nickname": data["nickname"],
            "name": data["name"],
            "email": data["email"],
            "avatar": data["picture"],
        }

    def revoke(self, token) -> bool:
        return
