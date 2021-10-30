class OAuthUser:
    def __init__(self):
        self.id = None
        self.name = None
        self.nickname = None
        self.email = None
        self.avatar = None
        self.token = None

    def set_token(self, token):
        self.token = token
        return self

    def build(self, raw_data):
        self.id = raw_data.get("id", None)
        self.name = raw_data.get("name", None)
        self.nickname = raw_data.get("nickname", None)
        self.email = raw_data.get("email", None)
        self.avatar = raw_data.get("avatar", None)
        return self
