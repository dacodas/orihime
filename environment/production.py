import os 
import re

## EDIT AFTER THIS LINE

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['orihime.dacodastrack.com',
                 'orihime-django.orihime']

GOO_LOCAL_HOST="http://mod-goo.orihime"

STATIC_ROOT = '/srv/orihime-django/static/'
DATABASE_PATH = "/var/lib/orihime-django/db.sqlite3"
DEBUG_LOG_PATH = '/var/log/orihime-django/debug.log'

## EDIT BEFORE THIS LINE

settings_regex = re.compile('[A-Z_]+$')
environment_settings = {k: v for k, v in locals().items() if settings_regex.match(k)}


