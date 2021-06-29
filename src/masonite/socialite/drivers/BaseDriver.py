from os.path import join
from requests_oauthlib import OAuth2Session
from masonite.exceptions import RouteNotFoundException


class BaseDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

        self._is_stateless = False
        self._scopes = []

    def set_options(self, options):
        self.options = options
        return self

    def get_absolute_redirect_uri(self):
        redirect_route_or_url = self.options.get("redirect")
        # convert to route with name
        try:
            redirect_url = self.application.make("router").route(redirect_route_or_url)
        except RouteNotFoundException:
            redirect_url = redirect_route_or_url

        # TODO: make abs path => how ? add helper in Masonite and APP_URL env variable ?
        return join("http://localhost:8000", redirect_url.lstrip("/"))

    def get_client(self):
        return OAuth2Session(
            client_id=self.options.get("client_id"), redirect_uri=self.get_absolute_redirect_uri()
        )

    def stateless(self):
        self._is_stateless = True
        return self

    def scopes(self, scopes_list):
        self._scopes.extend(scopes_list)
        return self

    def has_invalid_state(self):
        if self._is_stateless:
            return False
        state = self.application.make("session").get("state")
        return state != self.application.make("request").input("state")

    def get_auth_url(self):
        raise NotImplementedError()

    def get_token_url(self):
        raise NotImplementedError()

    def redirect(self):
        raise NotImplementedError()

    def user(self):
        raise NotImplementedError()
