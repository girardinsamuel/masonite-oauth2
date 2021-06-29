"""Socialite Settings"""
from masonite.environment import env

DRIVERS = {
    "github": {
        "client_id": env("GITHUB_CLIENT_ID"),
        "client_secret": env("GITHUB_CLIENT_SECRET"),
        "redirect": "auth.callback",
    },
    "gitlab": {
        "client_id": env("GITLAB_CLIENT_ID"),
        "client_secret": env("GITLAB_CLIENT_SECRET"),
        "redirect": "/auth/callback",
    },
}
