import os

from masonite.foundation import response_handler
from masonite.storage import StorageCapsule
from masonite.auth import Sign
from masonite.environment import LoadEnvironment
from masonite.utils.structures import load
from masonite.middleware import (
    SessionMiddleware,
    EncryptCookies,
    LoadUserMiddleware,
)
from masonite.routes import Route
from masonite.configuration.Configuration import Configuration
from masonite.configuration.helpers import config


class Kernel:

    http_middleware = [EncryptCookies]

    route_middleware = {
        "web": [SessionMiddleware, LoadUserMiddleware],
    }

    def __init__(self, app):
        self.application = app

    def register(self):
        # Register routes
        self.load_environment()
        self.register_configurations()
        self.register_middleware()
        self.register_routes()
        self.register_database()
        self.register_templates()
        self.register_storage()

    def load_environment(self):
        LoadEnvironment()

    def register_routes(self):
        Route.set_controller_module_location(self.application.make("controller.location"))
        self.application.make("router").add(
            Route.group(load("tests/integrations/web", "ROUTES", []), middleware=["web"])
        )

    def register_middleware(self):
        self.application.make("middleware").add(self.route_middleware).add(self.http_middleware)

    def register_configurations(self):
        # load configuration
        self.application.bind("config.location", "tests/integrations/config")
        configuration = Configuration(self.application)
        configuration.load()
        self.application.bind("config", configuration)
        # set locations
        self.application.bind("controller.location", "tests/integrations/controllers")
        self.application.bind("jobs.location", "tests/integrations/jobs")
        self.application.bind("providers.location", "tests/integrations/providers")
        self.application.bind("mailables.location", "tests/integrations/mailables")
        self.application.bind("listeners.location", "tests/integrations/listeners")
        self.application.bind("validation.location", "tests/integrations/validation")
        self.application.bind("notifications.location", "tests/integrations/notifications")
        self.application.bind("events.location", "tests/integrations/events")
        self.application.bind("tasks.location", "tests/integrations/tasks")

        self.application.bind("server.runner", "masonite.commands.ServeCommand.main")
        key = config("application.key")
        self.application.bind("key", key)
        self.application.bind("sign", Sign(key))

    def register_templates(self):
        self.application.bind("views.location", "tests/integrations/templates/")

    def register_database(self):
        from masoniteorm.query import QueryBuilder

        self.application.bind(
            "builder",
            QueryBuilder(connection_details=config("database.databases")),
        )

        self.application.bind("migrations.location", "tests/integrations/databases/migrations")
        self.application.bind("seeds.location", "tests/integrations/databases/seeds")

        from config.database import DB

        self.application.bind("resolver", DB)

    def register_storage(self):
        storage = StorageCapsule(self.application.base_path)
        storage.add_storage_assets(
            {
                # folder          # template alias
                "storage/static": "static/",
                "storage/compiled": "static/",
                "storage/uploads": "static/",
                "storage/public": "/",
            }
        )
        self.application.bind("storage_capsule", storage)

        self.application.set_response_handler(response_handler)
        self.application.use_storage_path(os.path.join(self.application.base_path, "storage"))
