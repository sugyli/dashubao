"""
Django settings for dashubao project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

from dashubao import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c19)#j-dzo$rzpni0kzdt8&xed!c5d4l^9-2#0)50o*%c_(b9j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

ALLOWED_HOSTS = config.allowed_hosts


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'novels',
    'users',
    'operation',
    'search',
    'crispy_forms',
    'django_hosts',
    'pure_pagination'

]
AUTH_USER_MODEL = "users.UserProfile"
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}
MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_hosts.middleware.HostsRequestMiddleware',
]
ROOT_HOSTCONF = 'dashubao.hosts'
DEFAULT_HOST = 'm'

ROOT_URLCONF = 'dashubao.urls'

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

                'django.template.context_processors.media',

                'dashubao.tp_global_variable.read_settings_file'
            ],
        },
    },
]

WSGI_APPLICATION = 'dashubao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.name,
        'USER': config.user,
        'PASSWORD': config.password,
        'HOST': config.host
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

"""
import logging
生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)
生成一个名为collect的logger实例
collect_logger = logging.getLogger("collect")
logger.debug("一个萌萌的请求过来了。。。。")
logger.info("一个更萌的请求过来了。。。。")
logger.debug("这是app01里面的index视图函数")
collect_logger.info("用户1:河南")

"""

if DEBUG:

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,  # 禁用已经存在的logger实例
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            # 针对 DEBUG = True 的情况
        },
        'formatters': {
            # 详细的日志格式
            'standard': {
                'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                          '[%(levelname)s][%(message)s]'
            },
            # 简单的日志格式
            'simple': {
                'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
            },
            # 定义一个特殊的日志格式
            'collect': {
                'format': '%(message)s'
            }
        },
        'handlers': {
            # 在终端打印
            'console': {
                'level': 'DEBUG',
                # 只有在Django debug为True时才在屏幕打印日志
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',  #
                'formatter': 'simple'
            },
            'default': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                # 日志文件
                'filename': os.path.join(BASE_DIR, "logs", 'default.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 3,  # 最多备份几个
                'formatter': 'standard',
                'encoding': 'utf-8',
            },  # 用于文件输出
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                # 日志文件
                'filename': os.path.join(BASE_DIR, "logs", 'error.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf-8',
            },
            # 专门定义一个收集特定信息的日志
            'collect': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                'filename': os.path.join(BASE_DIR, "logs", 'collect.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 5,
                'formatter': 'collect',
                'encoding': "utf-8"
            }

        },
        'loggers': {
            # 默认的logger应用如下配置
            '': {
                # 上线之后可以把'console'移除
                'handlers': ['default', 'console', 'error'],
                'level': 'DEBUG',
                'propagate': True,  # 向不向更高级别的logger传递
            },
            # 名为 'collect'的logger还单独处理
            'collect': {
                'handlers': ['console', 'collect'],
                'level': 'INFO',
            }
        },
    }
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,  # 禁用已经存在的logger实例
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
            # 针对 DEBUG = True 的情况
        },
        'formatters': {
            # 详细的日志格式
            'standard': {
                'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                          '[%(levelname)s][%(message)s]'
            },
            # 简单的日志格式
            'simple': {
                'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
            },
            # 定义一个特殊的日志格式
            'collect': {
                'format': '%(message)s'
            }
        },
        'handlers': {
            # 在终端打印
            'console': {
                'level': 'DEBUG',
                # 只有在Django debug为True时才在屏幕打印日志
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',  #
                'formatter': 'simple'
            },
            'default': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                # 日志文件
                'filename': os.path.join(BASE_DIR, "logs", 'default.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 3,  # 最多备份几个
                'formatter': 'standard',
                'encoding': 'utf-8',
            },  # 用于文件输出
            'error': {
                'level': 'ERROR',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                # 日志文件
                'filename': os.path.join(BASE_DIR, "logs", 'error.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 5,
                'formatter': 'standard',
                'encoding': 'utf-8',
            },
            # 专门定义一个收集特定信息的日志
            'collect': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                'filename': os.path.join(BASE_DIR, "logs", 'collect.log'),
                'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
                'backupCount': 5,
                'formatter': 'collect',
                'encoding': "utf-8"
            }

        },
        'loggers': {
            # 默认的logger应用如下配置
            '': {
                'handlers': ['default', 'error'],  # 上线之后可以把'console'移除
                'level': 'DEBUG',
                'propagate': True,  # 向不向更高级别的logger传递
            },
            # 名为 'collect'的logger还单独处理
            'collect': {
                'handlers': ['collect'],
                'level': 'INFO',
            }
        },
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
GLOBALSETTINGS = {
    'ADMIN_SITE_TITLE': '小说后台管理',
    'ADMIN_SITE_FOOTER': 'by sugyli 设计'
}


USER_LEVEL = [
    {'level': '1级', 'min': -9999999, 'max': 50, 'piao': 2},
    {'level': '2级', 'min': 50, 'max': 200, 'piao': 3},
    {'level': '3级', 'min': 200, 'max': 500, 'piao': 4},
    {'level': '4级', 'min': 500, 'max': 800, 'piao': 5},
    {'level': '5级', 'min': 800, 'max': 1200, 'piao': 6},
    {'level': '6级', 'min': 1200, 'max': 2000, 'piao': 7},
    {'level': '7级', 'min': 2000, 'max': 5000, 'piao': 8},
    {'level': '8级', 'min': 5000, 'max': 10000, 'piao': 9},
    {'level': '9级', 'min': 10000, 'max': 20000, 'piao': 10},
    {'level': '10级', 'min': 20000, 'max': 32000, 'piao': 11},
    {'level': '11级', 'min': 32000, 'max': 50000, 'piao': 12},
    {'level': '12级', 'min': 50000, 'max': 70000, 'piao': 13},
    {'level': '13级', 'min': 70000, 'max': 100000, 'piao': 14},
    {'level': '14级', 'min': 100000, 'max': 140000, 'piao': 15},
    {'level': '15级', 'min': 140000, 'max': 190000, 'piao': 16},
    {'level': '16级', 'min': 190000, 'max': 250000, 'piao': 17},
    {'level': '17级', 'min': 250000, 'max': 320000, 'piao': 18},
    {'level': '18级', 'min': 320000, 'max': 400000, 'piao': 19},
    {'level': '19级', 'min': 400000, 'max': 490000, 'piao': 20},
    {'level': '20级', 'min': 490000, 'max': 590000, 'piao': 21},
    {'level': '21级', 'min': 590000, 'max': 700000, 'piao': 22},
    {'level': '22级', 'min': 700000, 'max': 820000, 'piao': 23},
    {'level': '23级', 'min': 820000, 'max': 950000, 'piao': 24},
    {'level': '24级', 'min': 950000, 'max': 9999999, 'piao': 25}
]

USER_QIANDAO = [
    [{'t': 1, 'f': 20}, {'t': 2, 'f': 20}, {'t': 3, 'f': 20}, {'t': 4, 'f': 30}, {'t': 5, 'f': 30}],
    [{'t': 6, 'f': 30}, {'t': 7, 'f': 50}, {'t': 8, 'f': 30}, {'t': 9, 'f': 30}, {'t': 10, 'f': 30}],
    [{'t': 11, 'f': 30}, {'t': 12, 'f': 30}, {'t': 13, 'f': 30}, {'t': 14, 'f': 50}, {'t': 15, 'f': 30}],
    [{'t': 16, 'f': 30}, {'t': 17, 'f': 30}, {'t': 18, 'f': 30}, {'t': 19, 'f': 30}, {'t': 20, 'f': 30}],
    [{'t': 21, 'f': 50}, {'t': 22, 'f': 30}, {'t': 23, 'f': 30}, {'t': 24, 'f': 30}, {'t': 25, 'f': 30}],
    [{'t': 26, 'f': 30}, {'t': 27, 'f': 30}, {'t': 28, 'f': 50}, {'t': 29, 'f': 50}, {'t': 30, 'f': 50}]
]

WEB1_NAME = '大书包小说网'
WEB1_URL = 'https://www.51xunyue.com'
WAP1_NAME = '大书包小说手机网'
WAP1_URL = 'https://m.51xunyue.com'
DEF_FENMIAN = '/oldfenmian/noimg.jpg'
FENMIAN_URL = '/'
WAP_CHAPTER_LIST = 15
WEB_CHAPTER_LIST = 3000
SCT = 1200
EMAIL_V_URL = "51xunyue.com"





EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "m17355553110_1@163.com"
EMAIL_HOST_PASSWORD = config.email_host_password
# 另外EMAIL_USE_TLS是true的话，EMAIL_PORT不是25吧。
EMAIL_USE_TLS = False
EMAIL_FROM = EMAIL_HOST_USER

