web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --worker-class gevent --worker-connections 1000 --log-file -
worker: celery  -A config worker -l info

