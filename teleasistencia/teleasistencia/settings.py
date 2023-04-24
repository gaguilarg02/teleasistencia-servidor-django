"""
Django settings for teleasistencia project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar ciertas variables desde variables de sistema o el fichero "BASE_DIR/.env"
load_dotenv()

# Añadir la carpeta utilidad al path the python para poder usarlo como una libreria instalada con pip
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'utilidad'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6f@aenc^c_ba5@tqk@um!!areq#0f7ml#*2usa1t91ha(m3*_3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.0.2.2','localhost','127.0.0.1','192.168.0.12','*']

#Definimos el media root y medias url para que el servidor pueda mostrar la imagen
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'/teleasistenciaApp')



# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    #'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    #Django rest:
    'rest_framework',
    #Django rest framework social auth:
    'oauth2_provider',
        #'social_django',
        #'rest_framework_social_oauth2',
    #Rest con JWT:
    'rest_framework_simplejwt',

    # Para certificado https:
    "django_extensions",

    'teleasistenciaApp',
    # App para la notificación de alarmas
    'alarmasApp.apps.AlarmasAppConfig',
    # App para gestionar todos los tipos de eventos temporizados
    'schedulerApp.apps.SchedulerAppConfig'
]

ASGI_APPLICATION = 'teleasistencia.asgi.application'

# Para probar las alarmas sin necesidad del servidor Redis (sólo pruebas)
CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}

# En producción hay que usar un motor de almacenamiento Redis para alamacenar el Channel Layer
#CHANNEL_LAYERS = {
#    "default": {
#        "BACKEND": "channels_redis.core.RedisChannelLayer",
#        "CONFIG": {
#            "hosts": [("https://alumnos.iesvjp.es", 23844)],
#        },
#    },
#}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'teleasistenciaApp.middleware.LoggingMiddleware',
]

#Definimos las  variables de configuración del CORS
#	CORS_ALLOW_ALL_ORIGINS: En verdadero true permite que se hagan peticiones HTTP desde todos los orígenes
#	CORS_ALLOW_CREDENTIALS: en verdadero permite incluir cookies en las peticiones HTTP
#	CORS_ALLOWED_ORIGINS: Permite especificar desde que dominios se permiten las peticiones HTTP

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'https://localhost:8000',

]

ROOT_URLCONF = 'teleasistencia.urls'

#AUTH_USER_MODEL = 'teleasistenciaApp.User'

ALLOWED_IMAGE_TYPES = (
    "jpeg",
    "jpg",
    "png",
    "gif"
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #AÑADIR LA CARPETA DE TEMPLATES DE TELEASISTENCIA:
            os.path.join(BASE_DIR, 'teleasistenciaApp','templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # OAuth
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.media',
            ],
        },
    },
]

############# DJANGO REST SOCIAL AUTH WITH GOOGLE:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # OAuth
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # django-oauth-toolkit >= 1.0.0
        #'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.IsAuthenticated',
    ]
}

# Especificamos los timpos de validez del token
# Tambien el tipo de cabecera de ese token Bearer
SIMPLE_JWT = {
    # Lo más "correcto" es que el token de acceso tenga una duración relativamente
    # corta, de unos minutos, para que no sea de mucho uso si es robado.
    # Por otra parte, el token de refresco, sirve para obtener un nuevo token de accesow
    # cuando este deje de ser válido, por lo que lo normal es que este dure significativamente más.
    # TODO: hacer uso del refresh token en todos los clientes (revertir duración de los tokens)
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Facebook, OpenId, etc)
    # Google OAuth2
        #'social_core.backends.google.GoogleOAuth2',
    # django-rest-framework-social-oauth2
        'rest_framework_social_oauth2.backends.DjangoOAuth2',
    # Django
    'django.contrib.auth.backends.ModelBackend',
    'rest_framework_simplejwt.authentication.JWTAuthentication',
)

#Redirección tras login OK POR OAUTH2 (ELIMINAR CUANDO SE COMPRUEBE QUE NO PETA)
#LOGIN_REDIRECT_URL = 'teleasistenciaHome'
# Google configuration
#SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '221206471010-ngm6bsac6a0bjrggalm10noo8e0kae51.apps.googleusercontent.com'
#SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
#SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
#    'https://www.googleapis.com/auth/userinfo.email',
#    'https://www.googleapis.com/auth/userinfo.profile',
#]

##################FIN



WSGI_APPLICATION = 'teleasistencia.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# Password email reset (Fichero: BASE_DIR/.env)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

PASSWORD_RESET_TIMEOUT_DAYS = 1

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
