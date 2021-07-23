"""A WelcomeController Module."""
from masonite.views import View
from masonite.controllers import Controller

from src.masonite.socialite import Socialite


class WelcomeController(Controller):
    """WelcomeController Controller Class."""

    def show(self, view: View):
        return view.render("base")

    def auth(self):
        return Socialite.driver("google").redirect()

    def callback(self):
        user = Socialite.driver("google").user()
        user2 = Socialite.driver("google").user_from_token(user.token)
        # you now have a user object with data and a token
        return vars(user)
