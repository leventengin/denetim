

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY keep the secret key used in production secret!
SECRET_KEY = '0gd2u5e^uye5a5gvl!1p10=d35_z)y#gap11&f4%h7x4i0efqy'

# SECURITY: don't run with debug turned on in production!
DEBUG = True


ADMINS = [('admin', 'levent@ez-manage.org')]

ALLOWED_HOSTS = ['37.148.210.226',
                 '172.104.239.247',
                 '127.0.0.1']





EMAIL_HOST = 'mail.ez-manage.org'
EMAIL_HOST_USER = 'yonetici@ez-manage.org'
EMAIL_HOST_PASSWORD = 'TXhp74S0'
EMAIL_PORT = 587
EMAIL_USE_TLS = True



# using gmail you will need to unloack Captcha to enable Django, to send for you:
# https://accounts.google.com/displayunlockcaptcha


# Application definition

CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = [
    'islem',
    'notification',
    'webservice',
    'charts',
    'rest_framework',
    'bootstrap3',
    'searchableselect',
    'dal',
    'dal_select2',
    'timedeltatemplatefilter',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_forms_bootstrap',
    'django.contrib.postgres',
    'django.contrib.humanize',
    'django_select2',
    'jquery',
    'django_extensions',
    #'kronos',
    #'islem.apps.IslemConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'denetim.urls'
SESSION_EXPIRE_AT_BROWSER_CLOSE = 'True'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'denetim.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'denetim',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

DATE_INPUT_FORMATS = ('%d-%m-%Y')

LANGUAGES = [
    ('en-us', ('English')),
    ('tr', ('Turkish')),
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [ os.path.join(BASE_DIR, "static_cdn"),
                      #'/var/www/static/',
]

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

LOGIN_REDIRECT_URL = '/islem/'

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


ADR_LOCAL = '127.0.0.1:7000'
#ADR_LOCAL = '37.148.210.226'
#ADR_LOCAL = '172.104.239.247'


HTTP_LOC = '127.0.0.0:7000'
#HTTP_LOC = '37.148.210.226'
#HTTP_LOC = 'http://ez-manage.net'


USER_GLB = 'ez-admin'
PASW_GLB = 'ezadmincheck'
