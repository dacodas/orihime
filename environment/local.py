import os 
import re

## EDIT AFTER THIS LINE

DEBUG = True
SECRET_KEY = '&q!7k0dgbsxjj$eo4kcu%gmh&$ionu+93=#+=d_iy*&%)ct(h#'
ALLOWED_HOSTS = ['testserver',
                 '127.0.0.1']

GOO_LOCAL_HOST="http://localhost:8000"

LOCAL_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(LOCAL_ROOT, 'static/')
DATABASE_PATH = os.path.join(LOCAL_ROOT, 'local/db.sqlite3')
DEBUG_LOG_PATH = os.path.join(LOCAL_ROOT, 'local/debug.log')

## EDIT BEFORE THIS LINE

settings_regex = re.compile('[A-Z_]+$')
environment_settings = {k: v for k, v in locals().items() if settings_regex.match(k)}

