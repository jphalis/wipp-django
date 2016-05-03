import os
import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


MAX_MILE_DISTANCE = 200  # Maximum distance a trip can be in miles


# HOSTING + AUTHENTICATION
SECRET_KEY = '8vbhgb!qb=w_8be(hh(tqnorzc9wp7&+s)54n4g+6qxgbd)qwb'
LOGIN_URL = "/signin/"
AUTH_USER_MODEL = 'accounts.MyUser'
MIN_PASSWORD_LENGTH = 5
FULL_DOMAIN_NAME = ''


# E M A I L
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None


# I N T E R N A T I O N A L I Z A T I O N
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
USE_TZ = False

# Choices: INTERNATIONAL, E164, NATIONAL, RFC3966
# PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'


# A P P L I C A T I O N S
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'crispy_forms',
    'geopy',
    'rest_framework',
    'accounts',
    'api',
    'reservations',
)


# M I D D L E W A R E
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)


ROOT_URLCONF = 'wipp.urls'
WSGI_APPLICATION = 'wipp.wsgi.application'


# T E M P L A T E S
CRISPY_TEMPLATE_PACK = "bootstrap3"


# S E S S I O N S
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4 * 6  # six months
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# F I L E  U P L O A D S
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB


# A P I
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'SEARCH_PARAM': 'q',
}
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'core.utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=180),
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_SECRET_KEY': '8vbhgb!qb=w_8be(hh(tqnorzc9wp7&+s)54n4g+6qxgbd)qwb',
}
