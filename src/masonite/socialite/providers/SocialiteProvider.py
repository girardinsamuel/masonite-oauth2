"""A SocialiteProvider Service Provider."""
from masonite.providers import Provider
from masonite.socialite.commands.InstallCommand import InstallCommand
from masonite.utils.structures import load

from ..Socialite import Socialite
from ..drivers import GithubDriver, GitlabDriver, BitbucketDriver, GoogleDriver


class SocialiteProvider(Provider):
    """Provides Services To The Service Container."""

    def __init__(self, app):
        self.application = app

    def register(self):
        """Register objects into the Service Container."""
        self.application.make("commands").add(InstallCommand())
        self.application.bind("config.socialite", "masonite.socialite.config.socialite")
        socialite = Socialite(self.application).set_configuration(
            load(self.application.make("config.socialite")).DRIVERS
        )
        socialite.add_driver("github", GithubDriver(self.application))
        socialite.add_driver("gitlab", GitlabDriver(self.application))
        socialite.add_driver("bitbucket", BitbucketDriver(self.application))
        socialite.add_driver("google", GoogleDriver(self.application))
        self.application.bind("socialite", socialite)

    def boot(self):
        """Boots services required by the container."""
        pass
