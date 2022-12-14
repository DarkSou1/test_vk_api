import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ['web', 'localhost', 'dogdogmote.ddns.net', '127.0.0.1', ]

# Application definition

INSTALLED_APPS = [
    # django_apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # project_apps
    'sorl.thumbnail',
    'social_django',
    'users',
    'core',
    'vk_posts',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')

# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email', 'wall', 'photos', 'offline', 'groups', 'status',
#                                'friends', 'audio', 'video', 'pages', ]

# SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['notify', 'friends', 'photos', 'audio',
#                                'video', 'stories', 'pages', 'status',
#                                'notes', 'messages', 'wall', 'ads',
#                                'offline', 'docs', 'groups', 'notifications',
#                                'stats', 'email', 'market']

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['1073737727', ]

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_CREATE_USERS = True  # разрешает создавать пользователей через social_auth

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_uid',
    # Получить социальный uid из любой службы, через которую мы авторизуемся.
    'social_core.pipeline.social_auth.social_user',
    # Проверяет, привязана ли уже текущая социальная учетная запись к сайту.
    'social_core.pipeline.user.create_user',
    # Создайте учетную запись пользователя, если мы ее еще не нашли.
    'social_core.pipeline.user.user_details',
    # Обновите запись пользователя, указав любую измененную информацию из службы аутентификации
    'social_core.pipeline.social_auth.associate_user',
    # Создайте запись, которая связывает социальную учетную запись с пользователем.
    'social_core.pipeline.social_auth.load_extra_data',
    # Заполнить поле extra_data в социальной записи значениями
)

# LOGIN_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'good_heartst_project.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # 'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.cont'
            ],
        },
    },
]

WSGI_APPLICATION = 'good_heartst_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.getenv('ENGINE', default="django.db.backends.postgresql_psycopg2"),
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.MyUser'


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SCRIPT FOR VK_POSTS
COUNT_OF_POSTS = 100
PHOTO_SIZE = 4
TIME_SLEEP = 3600
