from urllib.parse import parse_qs, urlparse
from masonite.routes import Route
from masonite.tests import TestCase
from src.masonite.oauth import OAuth


class TestMethods(TestCase):
    def setUp(self):
        super().setUp()
        self.setRoutes(
            Route.get("/redirect-data", "WelcomeController@auth_with_data"),
            Route.get("/redirect-scopes", "WelcomeController@auth_with_scopes"),
        )

    def test_scopes(self):
        driver = OAuth.driver("github").scopes(["test:a"])
        assert driver._scopes == ["user:email", "test:a"]
        OAuth.driver("github").reset_scopes()

    def test_set_scopes(self):
        driver = OAuth.driver("github").set_scopes(["test:a"])
        assert driver._scopes == ["test:a"]
        OAuth.driver("github").reset_scopes()

    def test_with_data(self):
        driver = OAuth.driver("github").with_data({"user": "test"})
        assert driver._data == {"user": "test"}

    def test_request_with_additional_data(self):
        response = self.get("/redirect-data")
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)
        assert redirect_params.get("framework")[0] == "masonite"

    def test_request_with_additional_scope(self):
        response = self.get("/redirect-scopes")
        redirect_url = response.response.header("Location")
        data = urlparse(redirect_url)
        redirect_params = parse_qs(data.query)

        scopes = redirect_params.get("scope")[0]
        assert "user:email" in scopes
        assert "admin:org" in scopes
        OAuth.driver("github").reset_scopes()
