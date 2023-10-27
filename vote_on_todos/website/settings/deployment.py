"""Application settings for deployment."""
from __future__ import annotations

import os

from ._base import *  # noqa: F401, F403

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False

ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split(',')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
