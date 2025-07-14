import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG") == "True"
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    # Admin Style
    'jazzmin',


    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Custom
    'apps.customers',
    'apps.orders',
    'apps.products',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/'), 
        ],
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


WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": os.getenv("MYSQL_DB_NAME"),
        "USER": os.getenv("MYSQL_DB_USER"),
        "PASSWORD": os.getenv("MYSQL_DB_PASSWORD"),
        "HOST": os.getenv("MYSQL_DB_HOST"),
        "PORT": os.getenv("MYSQL_DB_PORT"),
    }
}

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

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATIC_ROOT = BASE_DIR / "staticfiles"
else:
    STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = False

X_FRAME_OPTIONS = 'SAMEORIGIN'


JAZZMIN_SETTINGS = {
    "site_title": "Sasori Imports",
    "site_header": "Sasori Imports",
    "site_brand": "Sasori Imports",
    'welcome_sign': 'Bem vindo ao painel de administração',
    'site_logo': '/img/akatsuki_cloud.png',
    'login_logo': '/img/akatsuki_cloud.png',
    'copyright': 'Sasori Imports',
    'show_ui_builder': True,

    "usermenu_links": [
        {"model": "auth.user"},
    ],

    "show_sidebar": True,
    "navigation_expanded": True,

    "order_with_respect_to": [
        "auth",
        "customers",
        "customers.customer",
        "customers.address",
        "orders",
        "orders.cart",
        "orders.cartitem",
        "orders.cartreference",
        "orders.order",
        "orders.token",
        "products",
        "products.category",
        "products.product",
        "products.productvariant",
        "products.productimage",
        "products.productreview",
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",

        "customers": "fas fa-user",
        "customers.customer": "fas fa-id-card",
        "customers.address": "fas fa-map-marker-alt",

        "orders": "fas fa-shopping-cart",
        "orders.cart": "fas fa-shopping-basket",
        "orders.cartitem": "fas fa-box-open",
        "orders.cartreference": "fas fa-link",
        "orders.order": "fas fa-receipt",
        "orders.token": "fas fa-key",

        "products": "fas fa-boxes",
        "products.category": "fas fa-tags",
        "products.product": "fas fa-box",
        "products.productvariant": "fas fa-cubes",
        "products.productimage": "fas fa-image",
        "products.productreview": "fas fa-star",
    },

    "related_modal_active": True,

    "changeform_format": "horizontal_tabs"
}
