web: gunicorn e_market.wsgi:application --log-file -
python manage.py collectstatic --noinput
manage.py migrate
