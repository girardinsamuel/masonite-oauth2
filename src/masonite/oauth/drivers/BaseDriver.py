import requests
from urllib.parse import urlencode

from masonite.exceptions import RouteNotFoundException
from masonite.facades import Url
from masonite.utils.str import random_string

from ..OAuthUser import OAuthUser


class BaseDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

        self._is_stateless = False
        self._scopes = self.get_default_scopes()
        self._data = {}
        self._scope_separator = ","

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
        return Url.url(redirect_url)

    def get_auth_params(self, state=None):
        params = {
            "client_id": self.options.get("client_id"),
            "redirect_uri": self.get_absolute_redirect_uri(),
            "scope": self.format_scopes(),
            "response_type": "code",
        }
        if self.use_state():
            params["state"] = state
        # add custom params
        params.update(self._data)

        return params

    def build_auth_url(self, state):
        params = self.get_auth_params(state)
        base_url = self.get_auth_url()
        query = urlencode(params)
        return f"{base_url}?{query}"

    def redirect(self, state=None):
        if self.use_state():
            # let user provide their own generated state
            state = state or self.get_state()
            # self.application.make("session").set("state", state)
            self.application.make("request").session.set("state", state)
        else:
            state = None
        authorization_url = self.build_auth_url(state)

        return self.application.make("response").redirect(location=authorization_url)

    def get_token_fields(self, code):
        fields = {
            "grant_type": "authorization_code",
            "client_id": self.options.get("client_id"),
            "client_secret": self.options.get("client_secret"),
            "code": code,
            "redirect_uri": self.get_absolute_redirect_uri(),
        }
        return fields

    def get_token(self):
        code = self.application.make("request").input("code")
        data = self.get_token_fields(code)
        response = requests.post(
            self.get_token_url(), data, headers={"Accept": "application/json"}
        )
        data = response.json()
        if response.status_code != 200:
            raise Exception("error")
        return data

    def stateless(self):
        self._is_stateless = True
        return self

    def use_state(self):
        return not self._is_stateless

    def get_state(self):
        return random_string(40)

    def scopes(self, scopes_list):
        self._scopes.extend(scopes_list)
        return self

    def set_scopes(self, scopes_list):
        self._scopes = scopes_list
        return self

    def has_scope(self, scope):
        return scope in self._scopes

    def format_scopes(self):
        self._scopes = list(set(self._scopes))
        # order list of scopes alphabetically
        self._scopes.sort()
        #
        return self._scope_separator.join(self._scopes)

    def with_data(self, data):
        """Add optional parameters in the redirect request that the provider might support.
        data should be a dict that will be converted into URL GET params."""
        self._data = data
        return self

    def has_invalid_state(self):
        if self._is_stateless:
            return False
        state = self.application.make("request").session.get("state")
        return state != self.application.make("request").input("state")

    def get_default_scopes(self) -> list:
        return []

    def reset_scopes(self):
        self._scopes = self.get_default_scopes()

    def get_auth_url(self):
        raise NotImplementedError()

    def get_token_url(self):
        raise NotImplementedError()

    def get_refresh_token_url(self):
        return self.get_token_url()

    def get_revoke_token_url(self):
        raise NotImplementedError()

    def get_user_url(self):
        raise NotImplementedError()

    def get_email_url(self):
        raise NotImplementedError()

    def get_request_options(self, *args):
        raise NotImplementedError()

    def map_user_data(self, data) -> "OAuthUser":
        raise NotImplementedError()

    def revoke(self, token) -> bool:
        raise NotImplementedError()

    def get_email_by_token(self, token):
        """E-mail is often not send directly with user info, a subsequent request needs to be
        made in order to fetch user e-mail (if scopes allow it)."""
        if self.get_email_url():
            response = requests.get(self.get_email_url(), **self.get_request_options(token))
            return response.json()
        else:
            return {}

    def user(self) -> "OAuthUser":
        if self.has_invalid_state():
            raise Exception("Invalid state")
        data = self.get_token()
        token = data.get("access_token")
        user = self.user_from_token(token)
        user.set_refresh_token(data.get("refresh_token")).set_expires_in(data.get("expires_in"))
        return user

    def user_from_token(self, token: str) -> "OAuthUser":
        response = requests.get(self.get_user_url(), **self.get_request_options(token))
        data = response.json()
        if response.status_code != 200:
            raise Exception("Provider API error")
        email = self.get_email_by_token(token)
        if email:
            data.update({"email": email})
        user = OAuthUser().build(self.map_user_data(data))
        user.set_token(token)
        return user

    def refresh(self, refresh_token: str) -> "OAuthUser":
        params = {
            "client_id": self.options.get("client_id"),
            "client_secret": self.options.get("client_secret"),
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "redirect_uri": self.get_absolute_redirect_uri(),
        }
        query = urlencode(params)
        url = f"{self.get_refresh_token_url()}?{query}"
        response = requests.post(url, headers={"Accept": "application/json"})
        if response.status_code != 200:
            raise Exception("Provider API error")
        data = response.json()
        token = data.get("access_token")
        user = self.user_from_token(token)
        user.set_refresh_token(data.get("refresh_token")).set_expires_in(data.get("expires_in"))
        return user

    def perform_request(self, token, method, url, **options):
        """Perform an authenticated request to the API on behalf on the user to which the given
        token belongs with the token as a 'Bearer' authentication token."""
        request_options = {
            **self.get_request_options(token),
            **options,
        }
        response = requests.request(method, url, **request_options)
        return response

    def perform_basic_request(self, method, url, **options):
        """Perform an authenticated request to the API on behalf on the user to which the given
        token belongs with Basic HTTP authentication."""
        request_options = {
            "auth": requests.auth.HTTPBasicAuth(
                self.options.get("client_id"), self.options.get("client_secret")
            ),
            **options,
        }
        response = requests.request(method, url, **request_options)
        return response
