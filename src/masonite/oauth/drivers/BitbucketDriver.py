from .BaseDriver import BaseDriver


class BitbucketDriver(BaseDriver):
    """
    doc
    https://confluence.atlassian.com/bitbucketserver/bitbucket-oauth-2-0-provider-api-1108483661.html
    https://developer.atlassian.com/cloud/bitbucket/oauth-2/
    """

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

    def map_user_data(self, data):
        return {
            "id": data["uuid"],
            "nickname": data["username"],
            "name": data["display_name"],
            "email": data.get("email", ""),
            "avatar": data["links"]["avatar"]["href"],
        }

    def revoke(self, token):
        response = self.perform_basic_request(
            "post",
            "https://bitbucket.org/site/oauth2/revoke",
            json={"token": token},
            headers={"Accept": "application/json"},
        )
        if response.status_code == 200:
            return True
        else:
            return False
