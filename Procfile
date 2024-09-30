web: gunicorn Event_Tracker.wsgi:application --chdir Event_Tracker --log-level debug --log-file - --timeout 120
worker: CELERY_WORKER_RUNNING=1 celery -A Event_Tracker worker --loglevel=info
runserver: cd Event_Tracker && python manage.py runserver 0.0.0.0:$PORT