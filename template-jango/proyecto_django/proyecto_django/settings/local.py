from .base import *
from decouple import config, Csv
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
  "default": {
    "ENGINE": config('DB_ENGINE', default='django.db.backends.postgresql'),
    "NAME": config('DB_NAME', default=''),
    "USER": config('DB_USER', default=''),
    "PASSWORD": config('DB_PASSWORD', default=''),
    "HOST": config('DB_HOST', default=''),
    "PORT": config('DB_PORT', default=''),
  }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
