from masonite.tests import TestCase
from src.masonite.socialite import Socialite


class TestScopes(TestCase):
    def test_scopes(self):
        driver = Socialite.driver("github").scopes(["test:a"])
        assert driver._scopes[-1] == "test:a"

    def test_set_scopes(self):
        driver = Socialite.driver("github").set_scopes(["test:a"])
        assert driver._scopes == ["test:a"]

    def test_with_data(self):
        driver = Socialite.driver("github").with_data({"user": "test"})
        assert driver._data == {"user": "test"}
