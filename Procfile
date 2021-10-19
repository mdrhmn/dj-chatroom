release: python manage.py migrate
web: daphne django_chat_channels_redis.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=django_chat_channels_redis.settings -v2