from .BaseDriver import BaseDriver


class AppleDriver(BaseDriver):
    def get_default_scopes(self):
        return ["name", "email"]

    def get_auth_url(self):
        return "https://appleid.apple.com/auth/authorize"

    def get_token_url(self):
        return "https://appleid.apple.com/auth/token"

    def map_user_data(self, data):
        return {
            "id": data["sub"],
            "nickname": data["nickname"],
            "name": data["name"],
            "email": data["email"],
            "avatar": data["picture"],
        }
