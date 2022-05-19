"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller
from masonite.request import Request

from src.masonite.oauth import OAuth


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        return view.render("base")

    def auth(self, request: Request):
        provider = request.param("provider")
        return OAuth.driver(provider).redirect()

    def auth_with_data(self):
        return OAuth.driver("github").with_data({"framework": "masonite"}).redirect()

    def auth_with_scopes(self):
        return OAuth.driver("github").scopes(["admin:org"]).redirect()

    def callback(self, request: Request):
        provider = request.param("provider")
        user = OAuth.driver(provider).user()
        # user2 = OAuth.driver("github").user_from_token(user.token)
        # you now have a user object with data and a token
        return vars(user)
