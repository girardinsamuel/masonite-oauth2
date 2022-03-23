class OAuth:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def driver(self, name):
        try:
            selected_driver = self.drivers[name]
        except KeyError:
            raise Exception(f"The driver {name} has not been registered as an OAuth driver.")
        return selected_driver.set_options(self.get_config_options(name))

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config.get(self.driver_config.get("default"), {})
        return self.driver_config.get(driver, {})
