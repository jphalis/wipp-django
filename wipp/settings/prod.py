from wipp.settings.common import *

import dj_database_url

DEBUG = True


# HOSTING + AUTHENTICATION
ADMINS = (
    # ("Chris", "c.haralampoudis@gmail.com"),
    # ("Q", "schunkqj@gmail.com"),
)
MANAGERS = ADMINS
ALLOWED_HOSTS = [
    'www.domain.com',
    'domain.com',
    '*.domain.com',
    '127.0.0.1',
    'pure-shelf-18585.herokuapp.com',
]
CORS_URLS_REGEX = r'^/hidden/secure/wipp/api/.*$'


# E M A I L
FROM_EMAIL = 'wipp.college@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'wipp.college@gmail.com'
EMAIL_HOST_PASSWORD = 'gotaglockinmyrarri'
EMAIL_PORT = 587


# S S L  S E C U R I T Y
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_SECONDS = 0
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# A P P L I C A T I O N S
INSTALLED_APPS += (
    'storages',
)


# D A T A B A S E
DATABASES = {
    'default': {  # get credentials from Heroku database creation
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd7nvtivsu7jeah',
        'USER': 'lozwrsdudriegz',
        'PASSWORD': 'phpQXg1yIWUwGxblscYa0p89Jr',
        'HOST': 'ec2-23-21-42-29.compute-1.amazonaws.com',
        'PORT': '5432',
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
DATABASES['default'] = dj_database_url.config()  # Heroku
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
DATABASES['default']['NAME'] = 'd7nvtivsu7jeah'
DATABASES['default']['USER'] = 'lozwrsdudriegz'
DATABASES['default']['PASSWORD'] = 'phpQXg1yIWUwGxblscYa0p89Jr'
DATABASES['default']['HOST'] = 'ec2-23-21-42-29.compute-1.amazonaws.com'
DATABASES['default']['PORT'] = '5432'
# Change 'extra' to 'default' if you move to AWS or other


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
        },
    },
]


# H T M L  M I N I F I C A T I O N
KEEP_COMMENTS_ON_MINIFYING = False
EXCLUDE_FROM_MINIFYING = ('^hidden/secure/wipp/admin/',)


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
CACHE_MIDDLEWARE_SECONDS = 12
CACHE_MIDDLEWARE_KEY_PREFIX = ''


# A W S
# STATICFILES_DIRS = (
#     os.path.join(os.path.dirname(BASE_DIR), 'static', 'static_dirs'),
# )
# AWS_ACCESS_KEY_ID = ''
# AWS_SECRET_ACCESS_KEY = ''
# AWS_STORAGE_BUCKET_NAME = ''
# S3DIRECT_REGION = 'us-east-1'
# AWS_CLOUDFRONT_DOMAIN = ''
# STATICFILES_STORAGE = 'wipp.s3utils.StaticRootS3BotoStorage'  # static files
# STATIC_S3_PATH = 'media/'
# DEFAULT_FILE_STORAGE = 'wipp.s3utils.MediaRootS3BotoStorage'  # media uploads
# DEFAULT_S3_PATH = 'static/'
# S3_URL = '//{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# # Without cloudfront
# MEDIA_URL = S3_URL + STATIC_S3_PATH
# STATIC_URL = S3_URL + DEFAULT_S3_PATH
# MEDIA_ROOT = '/home/ubuntu/domain.com/wipp/static/media'  # change to specific
# STATIC_ROOT = '/home/ubuntu/domain.com/wipp/static/static'  # change to specific

# # With cloudfront
# # MEDIA_URL = '//{}/{}'.format(AWS_CLOUDFRONT_DOMAIN, STATIC_S3_PATH)
# # STATIC_URL = '//{}/{}'.format(AWS_CLOUDFRONT_DOMAIN, DEFAULT_S3_PATH)

# AWS_FILE_EXPIRE = 200
# AWS_PRELOAD_METADATA = True
# AWS_S3_SECURE_URLS = True
# date_three_months_later = datetime.date.today() + datetime.timedelta(3 * 365 / 12)
# expires = date_three_months_later.strftime('%A, %d %B %Y 20:00:00 EST')
# AWS_HEADERS = {
#     'Expires': expires,
#     'Cache-Control': 'max-age=31536000',  # 365 days
# }

# H E R O K U
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'static')
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(BASE_DIR), 'static', 'static_dirs'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static', 'media')


# L O G G I N G
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    }
}
