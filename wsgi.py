"""
WSGI config for orihime project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys 

from django.core.wsgi import get_wsgi_application

project_path = "/usr/local/src/orihime-django"
if project_path not in sys.path:
    sys.path.insert(0, project_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orihime.settings')

# https://stackoverflow.com/questions/13174479/django-use-pdb-interactive-debug-for-wsgi-running-app
# https://github.com/django/django/blob/master/django/core/wsgi.py
# https://github.com/django/django/blob/master/django/core/handlers/wsgi.py

class Debugger:
    def __init__(self, object):
        self.__object = object

    def __call__(self, *args, **kwargs):
        import pdb, sys
        debugger = pdb.Pdb()
        debugger.use_rawinput = 0
        debugger.reset()
        sys.settrace(debugger.trace_dispatch)
        try:
            return self.__object(*args, **kwargs)
        finally:
            debugger.quitting = 1
            sys.settrace(None)

application = get_wsgi_application()
# application = Debugger(application)
