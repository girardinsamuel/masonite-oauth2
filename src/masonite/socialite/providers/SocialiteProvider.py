"""A SocialiteProvider Service Provider."""

from masonite.providers import Provider
from masonite.socialite.commands.InstallCommand import InstallCommand


class SocialiteProvider(Provider):
    """Provides Services To The Service Container."""

    def __init__(self, app):
        self.application = app

    def register(self):
        """Register objects into the Service Container."""
        self.application.make("commands").add(InstallCommand())

    def boot(self):
        """Boots services required by the container."""
        pass
