"""A SocialiteProvider Service Provider."""
from masonite.configuration import config
from masonite.packages import PackageProvider

from ..OAuth import OAuth
from ..drivers import (
    GithubDriver,
    GitlabDriver,
    BitbucketDriver,
    GoogleDriver,
    AppleDriver,
    FacebookDriver,
)


class OAuthProvider(PackageProvider):
    """ServiceProvider for OAuth package"""

    def configure(self):
        (self.root("masonite/oauth").name("oauth").config("config/oauth.py", publish=True))

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
