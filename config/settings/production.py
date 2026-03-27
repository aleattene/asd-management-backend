"""
Production settings for ASD Management project.
"""

import os

import environ

from .base import *  # noqa: F401, F403

DEBUG = False

# Raises ImproperlyConfigured if SECRET_KEY is not set in the environment
SECRET_KEY: str = environ.Env()("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DATABASE"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "true").lower() in ("true", "1", "yes")

# HSTS — env-driven to allow safe staging/first deploys.
# Enable preload only after confirming the entire domain surface is HTTPS-ready.
# WARNING: SECURE_HSTS_PRELOAD=true submits the domain to browser preload lists — hard to reverse.
SECURE_HSTS_SECONDS = environ.Env().int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv("SECURE_HSTS_INCLUDE_SUBDOMAINS", "true").lower() in ("true", "1", "yes")
SECURE_HSTS_PRELOAD = os.getenv("SECURE_HSTS_PRELOAD", "false").lower() in ("true", "1", "yes")

# Reverse proxy support (nginx/caddy forward HTTPS as HTTP internally).
# Enable only when a trusted reverse proxy is guaranteed to set/strip this header.
# WARNING: if the app is reachable without a proxy, this header can be spoofed.
if os.getenv("TRUST_PROXY_SSL_HEADER", "").lower() in ("true", "1", "yes"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
