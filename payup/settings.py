
import os
from pathlib import Path
from dotenv import load_dotenv



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@^2_$r$z)-t)xkz#$7vfum44^%elfvl3bc1wj#310woqjoz88p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '52e8-2409-40f3-109a-878f-ff98-25b8-67c-e469.ngrok-free.app','127.0.0.1','localhost',
    'chingup.vyntec.co','54.224.106.40']

CSRF_TRUSTED_ORIGINS = [
    "https://52e8-2409-40f3-109a-878f-ff98-25b8-67c-e469.ngrok-free.app",
    'http://chingup.vyntec.co',
    'https://chingup.vyntec.co',
    'http://54.224.106.40'
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "bootstrap5",
    "core",
    "payment",
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'payup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'payup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'assets')
STATICFILES_DIRS = [
    BASE_DIR/'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')

BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")


# # Chingup Configuration
NAME = os.environ.get('NAME')
DESCRIPTION = os.environ.get('DESCRIPTION')
IMAGE_URL = os.environ.get('IMAGE_URL')
QUERY_URL = os.environ.get('QUERY_URL')
PAYMENT_URL = os.environ.get('PAYMENT_URL')

CHINGUP_MERCHANT_ID = os.environ.get("MERCHANT_ID")
CHINGUP_MERCHANT_SANDBOX_ID = os.environ.get("MERCHANT_SANDBOX_ID")

CHINGUP_API_KEY = os.environ.get("API_KEY")
CHINGUP_API_KEY_SANDBOX = os.environ.get("API_KEY_SANDBOX")

CHINGUP_API_URL = os.environ.get("API_URL")
CHINGUP_API_URL_SANDBOX = os.environ.get("API_URL_SANDBOX")


# Chingup Configuration
# if DEBUG:
#     CHINGUP_MERCHANT_ID = os.environ.get("MERCHANT_SANDBOX_ID")
#     CHINGUP_API_KEY = os.environ.get("API_KEY_SANDBOX")
#     CHINGUP_API_URL = os.environ.get("API_URL_SANDBOX")
# else:
#     CHINGUP_MERCHANT_ID = os.environ.get("MERCHANT_ID")
#     CHINGUP_API_KEY = os.environ.get("API_KEY")
#     CHINGUP_API_URL = os.environ.get("API_URL")