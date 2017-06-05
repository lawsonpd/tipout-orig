"""
Django settings for budgettool project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('BTSECRET', '')
with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db/db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'poorman',
        'PASSWORD': 'channel12OI&',
        'HOST': '',
        'PORT': '',
    }
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# ADMINS = [('Peter', 'lawsonpd@gmail.com'),
#          ]

# SERVER_EMAIL = 'poorman@localhost'

ALLOWED_HOSTS = [
    'localhost',
    'tipout-app.herokuapp.com',
    'tipoutapp.com',
    'www.tipoutapp.com',
]


# Application definition

INSTALLED_APPS = [
    'tipout.apps.TipoutConfig',
    'tipout_demo.apps.TipoutDemoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'bootstrap3',
    'custom_auth.apps.CustomAuthConfig',
]

SITE_ID = 1

MIDDLEWARE_CLASSES = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'budgettool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'budgettool.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'custom_auth.TipoutUser'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
#
# Not sure if this stuff is needed with whitenoise

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bootstrap-3.3.6-dist/fonts'),
]

# STATICFILES_DIRS = [
#     '/tmp/static/tipout'
# ]

# Simplified static file serving
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Login redirect URL to override '/accounts/profile/'
LOGIN_REDIRECT_URL = '/budget/'

# Memcached
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

SESSIONS_ENGINE = 'django.contrib.sessions.backends.cached_db'

# from https://devcenter.heroku.com/articles/django-memcache#further-reading-and-resources
def get_cache():
    import os
    try:
        os.environ['MEMCACHE_SERVERS'] = os.environ['MEMCACHIER_SERVERS'].replace(',', ';')
        os.environ['MEMCACHE_USERNAME'] = os.environ['MEMCACHIER_USERNAME']
        os.environ['MEMCACHE_PASSWORD'] = os.environ['MEMCACHIER_PASSWORD']
        return {
            'default': {
                'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
                'TIMEOUT': 500,
                'BINARY': True,
                'OPTIONS': { 'tcp_nodelay': True }
            }
        }
    except:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
            }
        }

CACHES = get_cache()

with open(os.path.join(BASE_DIR, 'cache_hash_key.txt')) as f:
    CACHE_HASH_KEY = f.read().strip()

# CACHE_MIDDLEWARE_ALIAS

# CACHE_MIDDLEWARE_SECONDS = 60

# CACHE_MIDDLEWARE_KEY_PREFIX = ''

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR + 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

STRIPE_KEYS = {
    'secret_key': 'sk_live_VZuuKr51mjqssdIYBtNWU0nq',
    'publishable_key': 'pk_live_WLB0pXGykT9BM5tJ1EixjZF1',
    'test_sk': 'sk_test_GVCFYxcWaAZq3zBnEifLXeJd',
    'test_pk': 'pk_test_p5rrucKiZvMX19wKoUGVDbRd'
}

PLAID_KEYS = {
    'client_id': '5919b358bdc6a44cd258c7ed',
    'public_key': '24e9b020590bce48aa758fd7fd36cd',
    'secret': '767b09ba62146e8a0216e867356ea4'
}

EMAIL_HOST = 'tipoutapp.com'
EMAIL_PORT = '25'
