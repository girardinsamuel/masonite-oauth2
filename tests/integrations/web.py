""" Web Routes """
from masonite.routes import Route

ROUTES = [
    Route.get("/", "WelcomeController@show").name("welcome"),
    # Step 1
    Route.get("/auth/redirect", "WelcomeController@auth").name("auth.redirect"),
    # Step 2
    Route.get("/auth/callback", "WelcomeController@callback").name("auth.callback"),
]
