import os
from masonite.tests import TestCase


class TestInstallPackage(TestCase):
    def test_publish_package(self):
        (
            self.craft("package:publish", "oauth")
            .assertSuccess()
            .assertOutputContains("Config")
            .assertOutputContains("tests/integrations/config/oauth.py")
        )
        assert os.path.isfile("tests/integrations/config/oauth.py")
        os.remove("tests/integrations/config/oauth.py")
