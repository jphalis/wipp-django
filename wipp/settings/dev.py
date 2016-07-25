from wipp.settings.common import *


# HOSTING + AUTHENTICATION
DEBUG = True
ALLOWED_HOSTS = ['*']
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
CONFIG_DEFAULTS = {
    'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    'SQL_WARNING_THRESHOLD': 100,
}


# E M A I L
FROM_EMAIL = ''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587


# A P P L I C A T I O N S
INSTALLED_APPS += (
    'debug_toolbar',
    # 'phonenumber_field',
)

PUSH_NOTIFICATIONS_SETTINGS = {
    # "GCM_API_KEY": "<your api key>",
    # "GCM_POST_URL": "https://android.googleapis.com/gcm/send",
    # "GCM_MAX_RECIPIENTS": 1000,
    "APNS_HOST": "gateway.sandbox.push.apple.com",
    "APNS_CERTIFICATE": os.path.join(os.path.dirname(BASE_DIR),
                                     'push_notifications',
                                     'certificates',
                                     'apns_dev.pem'),
    # "APNS_PORT": 2195
}


# D A T A B A S E
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'wipp',
        'USER': 'jphalis',
        'PASSWORD': '',
        'HOST': "127.0.0.1",
        'PORT': '5432',
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# M I D D L E W A R E
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)


# T E M P L A T E S
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
            'string_if_invalid': 'INVALID EXPRESSION: %s',
        },
    },
]


# C A C H E
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            '127.0.0.1:11211',
        ],
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 8
CACHE_MIDDLEWARE_KEY_PREFIX = ''


# S T A T I C F I L E S
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'static')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'static', 'static_dirs'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'media')
