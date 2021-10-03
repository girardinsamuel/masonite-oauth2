import requests
import json
from os.path import join
from urllib.parse import urlencode
from requests_oauthlib import OAuth2Session
from masonite.exceptions import RouteNotFoundException


class BaseDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

        self._is_stateless = False
        self._scopes = self.get_default_scopes()
        self._data = {}

    def set_options(self, options):
        self.options = options
        return self

    def get_absolute_redirect_uri(self):
        redirect_route_or_url = self.options.get("redirect")
        if not redirect_route_or_url:
            raise Exception("You should specify a redirect route name or URI")
        # convert to route with name
        try:
            redirect_url = self.application.make("router").route(redirect_route_or_url)
        except RouteNotFoundException:
            redirect_url = redirect_route_or_url

        # TODO: make abs path => how ? add helper in Masonite and APP_URL env variable ?
        return join("http://localhost:8000", redirect_url.lstrip("/"))

    def get_client(self):
        self._scopes.sort()
        return OAuth2Session(
            client_id=self.options.get("client_id"),
            redirect_uri=self.get_absolute_redirect_uri(),
            scope=self._scopes,
        )

    def redirect(self):
        client = self.get_client()
        authorization_url, state = client.authorization_url(self.get_auth_url())
        # add optional parameters
        authorization_url += "&" + urlencode(self._data)
        self.application.make("session").set("state", state)
        return self.application.make("response").redirect(location=authorization_url)

    def get_token(self):
        code = self.application.make("request").input("code")
        client = self.get_client()
        response = client.fetch_token(
            self.get_token_url(),
            client_secret=self.options.get("client_secret"),
            code=code,
        )
        token = response.get("access_token")
        return client, token

    def stateless(self):
        self._is_stateless = True
        return self

    def scopes(self, scopes_list):
        self._scopes.extend(scopes_list)
        return self

    def set_scopes(self, scopes_list):
        self._scopes = scopes_list
        return self

    def has_scope(self, scope):
        return scope in self._scopes

    def with_data(self, data):
        """Add optional parameters in the redirect request that the provider might support.
        data should be a dict that will be converted into URL GET params."""
        self._data = data
        return self

    def has_invalid_state(self):
        if self._is_stateless:
            return False
        state = self.application.make("session").get("state")
        return state != self.application.make("request").input("state")

    def get_default_scopes(self):
        return []

    def reset_scopes(self):
        self._scopes = self.get_default_scopes()

    def get_auth_url(self):
        raise NotImplementedError()

    def get_token_url(self):
        raise NotImplementedError()

    def get_user_url(self):
        raise NotImplementedError()

    def get_email_url(self):
        raise NotImplementedError()

    def get_request_options(self, *args):
        raise NotImplementedError()

    def get_email_by_token(self, token):
        """E-mail is often not send directly with user info, a subsequent request needs to be
        made in order to fetch user e-mail (if scopes allow it)."""
        response = requests.get(self.get_email_url(), **self.get_request_options(token))
        email_data = json.loads(response.content.decode("utf-8"))
        return email_data

    def user(self):
        if self.has_invalid_state():
            raise Exception("Invalid state")
        client, token = self.get_token()
        response = client.get(self.get_user_url())
        user_data = json.loads(response.content.decode("utf-8"))
        return user_data, token

    def user_from_token(self, token):
        response = requests.get(self.get_user_url(), **self.get_request_options(token))
        user_data = json.loads(response.content.decode("utf-8"))
        return user_data
