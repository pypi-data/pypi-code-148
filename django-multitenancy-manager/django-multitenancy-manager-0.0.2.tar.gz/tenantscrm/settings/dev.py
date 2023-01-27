from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3*7!rm!!-!md83od&=0z$ff321g69))xjal4a)x^^^3*l)t-rt'


EMAIL_HOST = "smtp.zoho.com"
EMAIL_PORT = 987
EMAIL_HOST_USER = "bubblenoreply1@gmail.com"
EMAIL_HOST_PASSWORD = "khambane325"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "No Reply <bubblenoreply1@gmail.com>"

#X_FRAME_OPTIONS = 'ALLOW'
#HELPDESK_VIEW_A_TICKET_PUBLIC = False
#HELPDESK_SUBMIT_A_TICKET_PUBLIC= False

#EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend’"
#EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")


TENANT_USERS_DOMAIN = "localhost"



DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'tenants-portal',
        'USER': 'postgres',
        'PASSWORD': 'khambane325',
        'HOST': '127.0.0.1',
        'PORT': '5434',
        'TEST': {
            'NAME': 'test_tenants-portal',
        },
    }
}