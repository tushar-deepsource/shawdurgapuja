import os
from pathlib import Path

import dj_database_url
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',

    'colorfield',
    'easy_thumbnails',
    'filer',
    'mptt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware' ,
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'main.get_username.RequestMiddleware',
]

ROOT_URLCONF = 'puja.urls'

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

WSGI_APPLICATION = 'puja.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

dotenv_file = BASE_DIR / ".env"
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

    MEDIA_ROOT = BASE_DIR / 'media'
    if not os.path.exists(BASE_DIR / 'media'): os.makedirs(BASE_DIR / 'media')

    PRODUCTION_SERVER = False
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    DEBUG = True
    SECRET_KEY = '0ssv!ort)z+7ueg4b0*@qpxb-1a#eme!xu=e6-n%g(t++&0heo'
    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}

else:
    PRODUCTION_SERVER = True
    DEBUG = False

    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'gdstorage.storage.GoogleDriveStorage'

    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ['SECRET_KEY']
    MIDDLEWARE = [MIDDLEWARE[0]]+['whitenoise.middleware.WhiteNoiseMiddleware']+MIDDLEWARE[1:]
    INSTALLED_APPS=INSTALLED_APPS[0:-1]+['whitenoise.runserver_nostatic']+[INSTALLED_APPS[-1]]

##The filemanager
FILER_STORAGES = {
    'public': {
        'main': {
            'ENGINE': 'puja.storage.GoogleDriveStorageSystemPuja',
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'puja.storage.GoogleDriveStorageSystemPuja',
        },
    },
    'private': {
        'main': {
            'ENGINE': 'puja.storage.GoogleDriveStorageSystemPuja',
            'UPLOAD_TO': 'filer.utils.generate_filename.randomized',
            'UPLOAD_TO_PREFIX': 'filer_public',
        },
        'thumbnails': {
            'ENGINE': 'puja.storage.GoogleDriveStorageSystemPuja',
        },
    },
}

THUMBNAIL_HIGH_RESOLUTION = True
FILER_CANONICAL_URL = 'sharing/'

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'


# # Deployment check
if PRODUCTION_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"

if os.getenv('DATABASE_URL')[0] == 'm':
    DATABASES['default']['OPTIONS'] = {'init_command': 'SET default_storage_engine=InnoDB',}
