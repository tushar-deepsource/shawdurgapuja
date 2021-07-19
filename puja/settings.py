import os
from pathlib import Path

import dj_database_url
import dotenv
from django.utils.translation import ugettext_lazy as _

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
    'django.contrib.humanize',
    
    'django_admin_listfilter_dropdown',
    'colorfield',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware' ,
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'main.request_get_processor.RequestMiddleware',
    
    'django.middleware.cache.FetchFromCacheMiddleware'
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
    
    if not os.path.exists(BASE_DIR / 'media'): os.makedirs(BASE_DIR / 'media')

    PRODUCTION_SERVER = False
    ALLOWED_HOSTS = ['*']
    DEBUG = True
    SECRET_KEY = '0ssv!ort)z+7ueg4b0*@qpxb-1a#eme!xu=e6-n%g(t++&0heo'
    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}

else:
    import ast
    PRODUCTION_SERVER = True
    DEBUG = ast.literal_eval(os.environ['DEBUG'].strip('\n').capitalize())

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
    ALLOWED_HOSTS = ['*']
    SECRET_KEY = os.environ['SECRET_KEY']
    MIDDLEWARE = [MIDDLEWARE[0]]+['whitenoise.middleware.WhiteNoiseMiddleware']+MIDDLEWARE[1:]
    INSTALLED_APPS=INSTALLED_APPS[0:-1]+['whitenoise.runserver_nostatic']+[INSTALLED_APPS[-1]]


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

USE_L10N = True

USE_I18N = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/'

WHITENOISE_MAX_AGE = 9000
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = []

if os.path.isdir(MEDIA_ROOT): pass
else: os.mkdir(MEDIA_ROOT)


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

LANGUAGES = (
    ('bn', _('Bengali')),
    ('en', _('English')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

HOMECOMING = os.environ.get('HOMECOMING')
SHASHTI = os.environ.get('SHASHTI')
SAPTAMI = os.environ.get('SAPTAMI')
ASHTAMI = os.environ.get('ASHTAMI')
NAVAMI = os.environ.get('NAVAMI')
DASHAMI = os.environ.get('DASHAMI')
TEST = os.environ.get('TEST')
TOKEN = os.environ.get('TOKEN')

COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_FILTERS = {
    'css':[
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js':[
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = False
