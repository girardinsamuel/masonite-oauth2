"""A InstallCommand Command."""
import os
from cleo import Command


package_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class InstallCommand(Command):
    """
    Publish config file

    oauth:install
    """

    def handle(self):
        # publish config files
        # you could publish views, controllers, commands or assets here
        # you can also do it in boot() method of the provider with publishes()
        pass
