source venv/bin/activate && redis-server --port 7777 && celery -A tasks worker --loglevel=info &&uwsgi -s 127.0.0.1:8008 -w website
