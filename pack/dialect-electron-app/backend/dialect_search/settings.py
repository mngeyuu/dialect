import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'  # 生产环境请更改

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 生产环境设置为False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']  # 添加你的域名

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方应用
    'rest_framework',
    'django_filters',
    'corsheaders',
    # 自定义应用
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dialect_search.urls'

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

WSGI_APPLICATION = 'dialect_search.wsgi.application'

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dialect_search',
#         'USER': 'dialect_user',
#         'PASSWORD': 'mycmyc',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # 开发环境允许所有域名
# 生产环境指定允许的域名
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # 前端 Vue 项目的地址
]
import os
import sys

# 检测是否在打包环境中
if getattr(sys, 'frozen', False):
    # 在PyInstaller/Electron环境中
    BASE_DIR = os.path.dirname(sys.executable)
    # 在Windows上，使用用户数据目录存储数据
    if sys.platform == 'win32':
        import appdirs

        user_data_dir = appdirs.user_data_dir("core", "YourCompany")
        os.makedirs(user_data_dir, exist_ok=True)

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(user_data_dir, 'db.sqlite3'),
            }
        }
        MEDIA_ROOT = os.path.join(user_data_dir, 'media')
    else:
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # 在正常Python环境中
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
