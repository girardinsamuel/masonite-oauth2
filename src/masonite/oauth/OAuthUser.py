class OAuthUser:
    def __init__(self):
        self.id = None
        self.name = None
        self.nickname = None
        self.email = None
        self.avatar = None
        self.token = None
        self.refresh_token = None
        self.expires_in = None

    def set_token(self, token):
        self.token = token
        return self

    def set_refresh_token(self, token):
        self.refresh_token = token
        return self

    def set_expires_in(self, expires_in):
        self.expires_in = expires_in
        return self

    def build(self, raw_data):
        self.id = raw_data.get("id", None)
        self.name = raw_data.get("name", None)
        self.nickname = raw_data.get("nickname", None)
        self.email = raw_data.get("email", None)
        self.avatar = raw_data.get("avatar", None)
        self.refresh_token = raw_data.get("refresh_token", None)
        self.expires_in = raw_data.get("expires_in", None)
        return self
