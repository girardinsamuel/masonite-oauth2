"""A SocialiteProvider Service Provider."""
from masonite.providers import Provider
from masonite.socialite.commands.InstallCommand import InstallCommand
from masonite.configuration import config

from ..Socialite import Socialite
from ..drivers import (
    GithubDriver,
    GitlabDriver,
    BitbucketDriver,
    GoogleDriver,
    AppleDriver,
    FacebookDriver,
)


class SocialiteProvider(Provider):
    """Provides Services To The Service Container."""

    def __init__(self, app):
        self.application = app

    def register(self):
        """Register objects into the Service Container."""
        self.application.make("commands").add(InstallCommand())

        self.application.make("config").merge_with(
            "socialite", "masonite.socialite.config.socialite"
        )

        socialite = Socialite(self.application).set_configuration(config("socialite.drivers"))
        socialite.add_driver("github", GithubDriver(self.application))
        socialite.add_driver("gitlab", GitlabDriver(self.application))
        socialite.add_driver("bitbucket", BitbucketDriver(self.application))
        socialite.add_driver("google", GoogleDriver(self.application))
        socialite.add_driver("apple", AppleDriver(self.application))
        socialite.add_driver("facebook", FacebookDriver(self.application))
        self.application.bind("socialite", socialite)

    def boot(self):
        """Boots services required by the container."""
        pass
