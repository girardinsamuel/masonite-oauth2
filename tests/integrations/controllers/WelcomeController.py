"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from masonite.request import Request

from src.masonite.socialite import Socialite


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        return view.render("base")

    def auth(self, request: Request):
        provider = request.param("provider")
        return Socialite.driver(provider).redirect()

    def auth_with_data(self):
        return Socialite.driver("github").with_data({"framework": "masonite"}).redirect()

    def auth_with_scopes(self):
        return Socialite.driver("github").scopes(["admin:org"]).redirect()

    def callback(self, request: Request):
        provider = request.param("provider")
        user = Socialite.driver(provider).user()
        # user2 = Socialite.driver("github").user_from_token(user.token)
        # you now have a user object with data and a token
        return vars(user)
