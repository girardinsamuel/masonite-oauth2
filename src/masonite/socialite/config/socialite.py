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
    "bitbucket": {
        "client_id": env("BITBUCKET_CLIENT_ID"),
        "client_secret": env("BITBUCKET_CLIENT_SECRET"),
        "redirect": "/auth/callback",
    },
}
