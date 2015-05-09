# This file is the specification for the WSGI file for
# bae333.pythonanywhere.com/activites
# On the webserver, it should be placed in:
#/home/var/www/bae333_pythonanywhere.com

import os
import sys

path = '/home/bae333/BAE/BAEdjango'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BAEdjango.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
