release: python3 manage.py migrate
web: daphne django_chat_channels_redis.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python3 manage.py runworker channel_layer --settings=django_chat_channels_redis.settings -v2