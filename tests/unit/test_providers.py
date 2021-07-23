from urllib.parse import urlparse
from masonite.tests import TestCase
from masonite.routes import Route
import requests

from src.masonite.socialite import Socialite


class TestScopes(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            # Step 1
            Route.get("/auth/redirect", "WelcomeController@auth").name("auth.redirect"),
            # Step 2
            Route.get("/auth/callback", "WelcomeController@callback").name("auth.callback"),
        )

    def test_github(self):
        response = self.get("/auth/redirect").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        response = requests.get(redirect_url)
        import pdb

        pdb.set_trace()
