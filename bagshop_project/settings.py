import os
from pathlib import Path
import dj_database_url
from decouple import config

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Ключ безопасности и режим отладки
SECRET_KEY = config('SECRET_KEY', default='django-insecure-default-key-for-dev')
DEBUG = config('DEBUG', default=True, cast=bool)

ROOT_URLCONF = 'bagshop_project.urls'

# Настройка ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
if not DEBUG:
    ALLOWED_HOSTS.extend([
        '.up.railway.app',
        'django-project-production-8e78.up.railway.app'  # Ваш точный домен на Railway
    ])

# Порядок приложений строго зафиксирован во избежание ошибок с шаблонами админки
INSTALLED_APPS = [
    'django.contrib.admin',          
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Сторонние библиотеки
    'rest_framework',
    'corsheaders', 
    
    # Локальные приложения
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise строго после SecurityMiddleware
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Автоматическая настройка базы данных через URL (PostgreSQL на Railway / SQLite локально)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# Настройки CORS (для работы с фронтендом в продакшне)
if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        'https://railway.app',
    ]
CORS_ALLOW_CREDENTIALS = True

# Настройка шаблонов (APP_DIRS: True обязателен для поиска шаблонов админки)
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

# Статические файлы (CSS, JS, Картинки интерфейса)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Безопасное подключение локальной папки статики (защита от ошибок сборки)
STATIC_DIR = BASE_DIR / 'static'
if STATIC_DIR.exists():
    STATICFILES_DIRS = [STATIC_DIR]

# Современный формат конфигурации хранилищ для Django 4.2+ и WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Медиа файлы (Загружаемые пользователем картинки сумок)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Настройки безопасности для продакшна (HTTPS)
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Настройки почты (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '://gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@shop.com')

# Перенаправления авторизации
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/catalog/'
LOGOUT_REDIRECT_URL = '/catalog/'

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_TZ = True

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Доверенные источники для защиты от CSRF атак в продакшне
CSRF_TRUSTED_ORIGINS = [
    'https://railway.app',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
