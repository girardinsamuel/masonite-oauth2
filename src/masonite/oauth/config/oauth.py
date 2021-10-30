"""Socialite Settings"""
from masonite.environment import env

DRIVERS = {
    "github": {
        "client_id": env("GITHUB_CLIENT_ID"),
        "client_secret": env("GITHUB_CLIENT_SECRET"),
        "redirect": "/auth/callback/github",
    },
    "gitlab": {
        "client_id": env("GITLAB_CLIENT_ID"),
        "client_secret": env("GITLAB_CLIENT_SECRET"),
        "redirect": "/auth/callback/gitlab",
    },
    "bitbucket": {
        "client_id": env("BITBUCKET_CLIENT_ID"),
        "client_secret": env("BITBUCKET_CLIENT_SECRET"),
        "redirect": "/auth/callback/bitbucket",
    },
    "google": {
        "client_id": env("GOOGLE_CLIENT_ID"),
        "client_secret": env("GOOGLE_CLIENT_SECRET"),
        "redirect": "/auth/callback/google",
    },
    "apple": {
        "client_id": env("APPLE_CLIENT_ID"),
        "client_secret": env("APPLE_CLIENT_SECRET"),
        "redirect": "/auth/callback/apple",
    },
    "facebook": {
        "client_id": env("FACEBOOK_CLIENT_ID"),
        "client_secret": env("FACEBOOK_CLIENT_SECRET"),
        "redirect": "/auth/callback/facebook",
    },
}
