import json
import os

# DEBUG = True

DEBUG = os.environ.get('MODE') == 'DEBUG'
STORAGE_S3 = os.environ.get('STORAGE') == 'S3' or DEBUG is False
DB_RDS = os.environ.get('DB') == 'RDS'

print('DEBUG : {}'.format(DEBUG))
print('STORAGE_S3 : {}'.format(STORAGE_S3))
print('DB_RDS : {}'.format(DB_RDS))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONF_DIR = os.path.join(ROOT_DIR, '.conf-secret')
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

CONFIG_FILE_COMMON = os.path.join(CONF_DIR, 'settings_common.json')

CONFIG_FILE = os.path.join(CONF_DIR, 'settings_local.json' if DEBUG else 'settings_deploy.json')

config_common = json.loads(open(CONFIG_FILE_COMMON).read())
config = json.loads(open(CONFIG_FILE).read())

for key, key_dict in config_common.items():
    if not config.get(key):
        config[key] = {}
    for inner_key, inner_key_dict in key_dict.items():
        config[key][inner_key] = inner_key_dict
print(config)

# AWS
AWS_ACCESS_KEY_ID = config['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config['aws']['secret_access_key']

AWS_S3_HOST = 's3.{}.amazonaws.com'.format(config['aws']['s3_region'])
AWS_S3_SIGNATURE_VERSION = config['aws']['s3_signature_version']
AWS_STORAGE_BUCKET_NAME = config['aws']['s3_storage_bucket_name']
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

# STATIC
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_DIR,
)

if STORAGE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'deploy_ec2.storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    STATIC_URL = 'https://{custom_domain}/{staticfiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        staticfiles_location=STATICFILES_LOCATION
    )

    DEFAULT_FILE_STORAGE = 'deploy_ec2.storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'
    MEDIAFILES_URL = 'https://{custom_domain}/{mediafiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        mediafiles_location=MEDIAFILES_LOCATION
    )


else:
    STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root')
    STATIC_URL = '/static/'

SECRET_KEY = config['django']['secret_key']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

AUTH_USER_MODEL = 'member.MyUser'

ALLOWED_HOSTS = config['django']['allowed_hosts']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'member',
    'storages',
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

ROOT_URLCONF = 'deploy_ec2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'deploy_ec2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if DEBUG and DB_RDS:
    config_db = config['db_rds']
else:
    config_db = config['db']
DATABASES = {
    'default': {
        'ENGINE': config_db['engine'],
        'NAME': config_db['name'],
        'USER': config_db['user'],
        'PASSWORD': config_db['password'],
        'HOST': config_db['host'],
        'PORT': config_db['port']
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
