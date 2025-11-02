import os
import sys
from pathlib import Path

# Добавляем src в путь Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from .settings import *

# Override settings for testing
DEBUG = False

# Use SQLite for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password hashers for faster tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Email backend for testing
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable logging for tests
LOGGING_CONFIG = None

# Test secret key
SECRET_KEY = 'test-secret-key-for-ci-cd-pipeline-only'

# Allow all hosts for testing
ALLOWED_HOSTS = ['*']

# Disable SSL for testing
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False