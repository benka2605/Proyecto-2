"""
Django settings for GameSmashrooms project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o462$wx9gi^_r)mw^&-67rie3n#mynrtw+!+aiw8a+!p%g&502'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['.vercel.app','127.0.0.1']


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'admin_confirm',
    'multi_captcha_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    'crispy_bootstrap4',
    'axes',
    'captcha',
    'django_recaptcha',
    'rest_framework',
    'cloudinary',
    'cloudinary_storage',
]


EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "tomyxdlol577@gmail.com"
EMAIL_HOST_PASSWORD = "jawo zvzd dxai qvrz"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"



#config admin captcha
MULTI_CAPTCHA_ADMIN = {
    'engine': 'simple-captcha',
}

# RECAPTCHA
RECAPTCHA_PUBLIC_KEY = '6LetsvUpAAAAAEZXXPFTkzNR0oZCNyIy8YIgXYMe'
RECAPTCHA_PRIVATE_KEY = '6LetsvUpAAAAAP1pNpccKyCvJFa9ZzaXLfATmEg2'

CRISPY_TEMPLATE_PACK = 'bootstrap4'
X_FRAME_OPTIONS = "SAMEORIGIN"

# CONFIGURACION DE AXES
AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]


#CONFIGURACIONES AXES
AXES_FAILURE_LIMIT = 3 #NUMERO DE INTENTOS FALLIDOS
AXES_COOLOFF_TIME = timedelta(minutes=1) # TIEMPO DE ESPERA ANTES DE PERMITIR OTRO INTENTO
AXES_LOCKOUT_URL = '/bloqueo/' # URL A LA QUE SE REDIRIGE CUANDO LA CUENTA SE BLOQUEA
AXES_RESET_ON_SUCCESS = True # RESTAVLECEMOS EL CONTADOR DE INTENTOS FALLIDOS CUANDO SE LOGEA CORRECTAMENTE

ROOT_URLCONF = 'GameSmashrooms.urls'

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

WSGI_APPLICATION = 'GameSmashrooms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST' : 'aws-0-sa-east-1.pooler.supabase.com',
        'NAME' : 'postgres',
        'USER' : 'postgres.cfiuyocdkmswtrrbzrup',
        'PASSWORD' : 'T0myxdlol#2024',
        'PORT' : '5432',

    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'





CLOUDINARY_STORAGE = {
    'CLOUD_NAME':'de64coy5w',
    'API_KEY':'637756129325518',
    'API_SECRET':'lvBRQjMSCJgC9GmRbZNEWqQd03c'
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'






# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

