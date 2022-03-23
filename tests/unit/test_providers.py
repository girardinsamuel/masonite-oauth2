import requests
from urllib.parse import urlparse, parse_qs
from masonite.tests import TestCase
from masonite.routes import Route


class TestProviders(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            # Step 1
            Route.get("/auth/redirect/@provider", "WelcomeController@auth").name("auth.redirect"),
            # Step 2
            Route.get("/auth/callback/@provider", "WelcomeController@callback").name(
                "auth.callback"
            ),
        )

    def test_apple(self):
        response = self.get("/auth/redirect/apple").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "appleid.apple.com"
        assert redirect_uri == "http://localhost:8000/auth/callback/apple"
        response.assertSessionHas("state", state)
        provider_response = requests.get(redirect_url)
        assert provider_response.status_code == 200

    def test_github(self):
        response = self.get("/auth/redirect/github").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "github.com"
        assert redirect_uri == "http://localhost:8000/auth/callback/github"
        response.assertSessionHas("state", state)
        provider_response = requests.get(redirect_url)
        assert provider_response.status_code == 200

    def test_gitlab(self):
        response = self.get("/auth/redirect/gitlab").assertRedirect()
        redirect_url = response.response.header("Location")
        print(redirect_url)
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "gitlab.com"
        assert redirect_uri == "http://localhost:8000/auth/callback/gitlab"
        response.assertSessionHas("state", state)
        # browser checks prevent us to check url during test => 503

    def test_google(self):
        response = self.get("/auth/redirect/google").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "accounts.google.com"
        assert redirect_uri == "http://localhost:8000/auth/callback/google"
        response.assertSessionHas("state", state)
        provider_response = requests.get(redirect_url)
        assert provider_response.status_code == 200

    def test_bitbucket(self):
        response = self.get("/auth/redirect/bitbucket").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "bitbucket.org"
        assert redirect_uri == "http://localhost:8000/auth/callback/bitbucket"
        response.assertSessionHas("state", state)

    def test_facebook(self):
        response = self.get("/auth/redirect/facebook").assertRedirect()
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        redirect_uri = redirect_params.get("redirect_uri")[0]
        state = redirect_params.get("state")[0]
        assert data.netloc == "www.facebook.com"
        assert redirect_uri == "http://localhost:8000/auth/callback/facebook"
        response.assertSessionHas("state", state)
        provider_response = requests.get(redirect_url)
        assert provider_response.status_code == 200
