from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-p@ty54s(-j8qjphym5txsr0uh2=%2hj&^t6a7-b06$4-^ba&eh"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ['https://*.gitpod.io']

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
