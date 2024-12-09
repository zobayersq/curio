import os
from pathlib import Path
from dotenv import load_dotenv
import environ
import dj_database_url
import requests
import ssl


load_dotenv()
# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, True),
)
environ.Env.read_env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-default-secret-key')  # Change this to an actual secret key for development only!

# SECURITY WARNING: Don't run with debug turned on in production!
DEBUG = env('DEBUG', default=True)

# Allowed hosts for production
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', default='localhost').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'widget_tweaks',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'curio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'curio.wsgi.application'

# Database configuration

'''
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'postgres://user:password@localhost:5432/dbname')
    )
}'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# Ensure you have a directory to collect your static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Optional: WhiteNoise configuration (this helps with caching, compression, etc.)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Security settings

#import requests
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
#if DEBUG:
#    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Your request here
#response = requests.get('https://example.com', verify=False)


# Ignore SSL certificate verification in development
#if settings.DEBUG:
#    response = requests.get('https://example.com', verify=False)
#else:
#    response = requests.get('https://example.com')

SECURE_SSL_REDIRECT = False  # Ensures HTTPS in production
SECURE_HSTS_SECONDS = 31536000  # 1 year (be careful using this before SSL is active)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

CSRF_COOKIE_SECURE = True  # Ensure the CSRF cookie is only sent over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Helps prevent client-side access to CSRF token

SESSION_COOKIE_SECURE = True  # Ensures the session cookie is only sent over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Helps prevent client-side access to session data

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Custom user model
AUTH_USER_MODEL = 'blog.CustomUser'

# Login URL
LOGIN_URL = '/login/'

# Additional settings for automatic primary key fields
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
