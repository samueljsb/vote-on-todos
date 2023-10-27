"""Settings to use for local development and testing.

These settings are less secure so should not be used for deployment.
"""
from __future__ import annotations

from ._base import *  # noqa: F401, F403

SECRET_KEY = 'django-insecure-n!+c@68u9*7w$bwl6td%stg4vu7t#bbu#j4mqh%(n6b)50&)'

DEBUG = True

ALLOWED_HOSTS: list[str] = ['*']
