import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puja.settings')

os.environ['ASYNC_RUN'] = 'False'
application = get_wsgi_application()
