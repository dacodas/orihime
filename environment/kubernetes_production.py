import os 
import re

import itertools 

release = os.environ['ORIHIME_RELEASE']
namespace = os.environ['ORIHIME_NAMESPACE']

## EDIT AFTER THIS LINE

fullname = 'orihime-django-{}'.format(release)

hostnames = list(itertools.accumulate(
    [fullname, namespace, 'svc', 'cluster', 'local'], 
    lambda x, y: '{}.{}'.format(x, y)
))

hostnames = hostnames + ["orihime.dacodastrack.com",
                         "xn--t8j3dxb8a.xn--q9jyb4c"]

DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
ALLOWED_HOSTS = hostnames 

GOO_LOCAL_HOST="http://mod-goo-{}.{}.svc".format(release, namespace)

# These are mounted from the host...
STATIC_ROOT = '/srv/orihime-django/static/'
DATABASE_PATH = "/var/lib/orihime-django/db.sqlite3"
DEBUG_LOG_PATH = '/var/log/orihime-django/debug.log'

## EDIT BEFORE THIS LINE

settings_regex = re.compile('[A-Z_]+$')
environment_settings = {k: v for k, v in locals().items() if settings_regex.match(k)}
