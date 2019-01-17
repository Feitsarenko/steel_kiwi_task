from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_shop',
        'USER': 'admin',
        'PASSWORD': os.environ['DATABASES_DEV_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '',
    }
}

