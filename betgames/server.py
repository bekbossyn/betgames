from .settings import *

STATIC_ROOT = '/home/static/'
MEDIA_ROOT = '/home/media/'


if not os.path.exists("logs"):
    os.makedirs("logs")


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'betgames',
        'USER': 'betgames',
        'PASSWORD': 'betgames',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s path: %(pathname)s module: %(module)s method: %(funcName)s  row: %(lineno)d message: %(message)s'
        },
        'simple': {
            'format': '[%(levelname)s] %(message)s'
        },
    },
    'handlers': {
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/main.log'),
            'maxBytes': 1024*1024*15,   # 15MB
            'backupCount': 10,
            'formatter': 'verbose'
        },

        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
        # 'error': {
        #     'level': 'ERROR',
        #     'filename': 'logs/error.log',
        #     'class': 'django.utils.log.AdminEmailHandler',
        # }
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins', 'info'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


DEBUG = False
