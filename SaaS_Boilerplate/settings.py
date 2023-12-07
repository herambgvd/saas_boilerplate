import os
from pathlib import Path

from django.contrib.messages import constants as messages
from dotenv import load_dotenv
from storages.backends.s3boto3 import S3Boto3Storage

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost', 'gvd.localhost', 'vidinsights.cloud',
                 'gvd.vidinsights.cloud',
                 'airtel.vidinsights.cloud', 'airtel.localhost']

CSRF_TRUSTED_ORIGINS = [
	'https://vidinsights.cloud',
	'https://gvd.vidinsights.cloud',
	'https://airtel.vidinsights.cloud',
]

# CORS_ORIGIN_ALLOW_ALL = True

# Application definition

SHARED_APPS = [
	'django_tenants',
	'tenant',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	# Packages
	'allauth',
	'allauth.account',
	'widget_tweaks',
	# Apps
	'public.home'
]

TENANT_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	# Packages
	'allauth',
	'allauth.account',
	'widget_tweaks',
	'guardian',
	'rest_framework',
	# Common Apps
	'tenantApps.common.base',
	'tenantApps.common.branch',
	'tenantApps.common.staff',
	# Neubit Apps
	'tenantApps.neubit.infrastructure',
	'tenantApps.neubit.monitoring',
	'tenantApps.neubit.surveillance',
	'tenantApps.neubit.notify',
	# Clarify Apps
	'tenantApps.clarify.marketplace',
	'tenantApps.clarify.alerts'
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "tenant.Client"
TENANT_DOMAIN_MODEL = "tenant.Domain"

MIDDLEWARE = [
	'django_tenants.middleware.main.TenantMainMiddleware',
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'allauth.account.middleware.AccountMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
	# ...
	"127.0.0.1",
	# ...
]

ROOT_URLCONF = "SaaS_Boilerplate.urls_tenants"
PUBLIC_SCHEMA_URLCONF = "SaaS_Boilerplate.urls_public"

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'SaaS_Boilerplate.wsgi.application'
# ASGI_APPLICATION = 'SaaS_Boilerplate.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASE_ROUTERS = (
	'django_tenants.routers.TenantSyncRouter',
)

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django_tenants.postgresql_backend',
# 		'NAME': 'saas-django',
# 		'USER': 'postgres',
# 		'PASSWORD': 'Hanu@0542',
# 		'HOST': 'localhost',
# 		'PORT': '5432',
# 	}
# }

DATABASES = {
	'default': {
		'ENGINE': 'django_tenants.postgresql_backend',
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USER'),
		'PASSWORD': os.environ.get('DB_PROD_PASSWORD'),
		'HOST': os.environ.get('DB_HOST'),
		'PORT': os.environ.get('DB_PORT'),
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

AUTHENTICATION_BACKENDS = [
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
	'guardian.backends.ObjectPermissionBackend'
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


# Static files (CSS, JavaScript, Images)

class StaticStorage(S3Boto3Storage):
	location = 'static'


class MediaStorage(S3Boto3Storage):
	location = 'media'


# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles"
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media/'
# DEFAULT_FILE_STORAGE = "django_tenants.files.storage.TenantFileSystemStorage"
# MULTITENANT_RELATIVE_MEDIA_ROOT = "%s"

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.ap-south-1.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'SaaS_Boilerplate.settings.MediaStorage'
STATICFILES_STORAGE = 'SaaS_Boilerplate.settings.StaticStorage'

## Message Tags ##
MESSAGE_TAGS = {
	messages.DEBUG: "alert-info",
	messages.INFO: "alert-info",
	messages.SUCCESS: "alert-success",
	messages.WARNING: "alert-warning",
	messages.ERROR: "alert-danger",
}

#  All Auth Configurations
LOGIN_REDIRECT_URL = "/ai/dashboard/"
LOGIN_URL = "account_login"
ACCOUNT_LOGOUT_ON_GET = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional"  # optional
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 3
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_ADAPTER = 'SaaS_Boilerplate.utils.adapters.CustomAccountAdapter'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Use SMTP email backend
EMAIL_HOST = 'smtp.googlemail.com'  # Gmail's SMTP server
EMAIL_PORT = 465  # Port for SSL 587 for TLS
DEFAULT_FROM_EMAIL = 'appliedmleasy@gmail.com'  # Default from email, replace with your email address
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')  # Get email host user from environment variable
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')  # Get email host password from environment variable
EMAIL_USE_TLS = False  # Do not use TLS
EMAIL_USE_SSL = True  # Use SSL for secure email transmission

# Setup Configurations
ACCOUNT_FORMS = {
	"login": "SaaS_Boilerplate.utils.forms.UserLoginForm",
	"signup": "SaaS_Boilerplate.utils.forms.UserRegistrationForm",
	"change_password": "SaaS_Boilerplate.utils.forms.PasswordChangeForm",
	"set_password": "SaaS_Boilerplate.utils.forms.PasswordSetForm",
	"reset_password": "SaaS_Boilerplate.utils.forms.PasswordResetForm",
	"reset_password_from_key": "SaaS_Boilerplate.utils.forms.PasswordResetKeyForm",
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging configuration
# LOGGING = {
# 	'version': 1,
# 	'disable_existing_loggers': False,
# 	'formatters': {
# 		'verbose': {
# 			'format': '{levelname} {asctime} {module} {message}',
# 			'style': '{',
# 		},
# 		'simple': {
# 			'format': '{levelname} {message}',
# 			'style': '{',
# 		},
# 	},
# 	'handlers': {
# 		'file': {
# 			'level': 'DEBUG',
# 			'class': 'logging.handlers.RotatingFileHandler',
# 			'filename': 'debug.log',
# 			'maxBytes': 1024 * 1024 * 5,  # 5 MB
# 			'backupCount': 5,
# 			'formatter': 'verbose',
# 		},
# 		'console': {
# 			'class': 'logging.StreamHandler',
# 			'formatter': 'simple',
# 		},
# 	},
# 	'loggers': {
# 		'django': {
# 			'handlers': ['file', 'console'],
# 			'level': 'DEBUG',
# 			'propagate': True,
# 		},
# 		'your_app_label': {
# 			'handlers': ['file', 'console'],
# 			'level': 'DEBUG',
# 			'propagate': False,
# 		},
# 	},
# }
