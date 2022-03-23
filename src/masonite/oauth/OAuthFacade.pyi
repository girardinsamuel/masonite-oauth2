from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .drivers.BaseDriver import BaseDriver


class OAuth:

    def add_driver(self, name:str, driver:"BaseDriver"):
        """Register a new driver for OAuth2."""
        ...

    def set_configuration(self, config:dict) -> OAuth:
        """Set configuration for OAuth2."""
        ...

    def driver(self, name:str) -> "BaseDriver":
        """Get OAuth2 instance for given driver."""
        ...

    def get_config_options(self, driver:str=None) -> dict:
        """Get configuration options for a given driver or the default driver."""
        ...
