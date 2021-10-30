"""A SocialiteProvider Service Provider."""
from masonite.providers import Provider
from masonite.configuration import config

from ..OAuth import OAuth
from ..drivers import (
    GithubDriver,
    GitlabDriver,
    BitbucketDriver,
    GoogleDriver,
    AppleDriver,
    FacebookDriver,
)
from ..commands import InstallCommand


class OAuthProvider(Provider):
    """Provides Services To The Service Container."""

    def __init__(self, app):
        self.application = app

    def register(self):
        """Register objects into the Service Container."""
        self.application.make("commands").add(InstallCommand())

        self.application.make("config").merge_with("oauth", "masonite.oauth.config.oauth")

        oauth = OAuth(self.application).set_configuration(config("oauth.drivers"))
        oauth.add_driver("github", GithubDriver(self.application))
        oauth.add_driver("gitlab", GitlabDriver(self.application))
        oauth.add_driver("bitbucket", BitbucketDriver(self.application))
        oauth.add_driver("google", GoogleDriver(self.application))
        oauth.add_driver("apple", AppleDriver(self.application))
        oauth.add_driver("facebook", FacebookDriver(self.application))
        self.application.bind("oauth", oauth)

    def boot(self):
        """Boots services required by the container."""
        pass
