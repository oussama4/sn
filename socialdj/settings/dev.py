from .base import *

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
""" CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8080/',
    'http://127.0.0.1:8000/'
] """

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
)

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000'
]