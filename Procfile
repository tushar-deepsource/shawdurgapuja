web: gunicorn  puja.asgi:application -k puja.workers.DynamicUvicornWorker
worker: celery -A puja worker  -l info -E
