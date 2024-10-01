web: gunicorn Event_Tracker.wsgi:application --chdir Event_Tracker --log-level debug --log-file - --timeout 120
worker: celery -A Event_Tracker.celery worker --loglevel=info
runserver: cd Event_Tracker && python manage.py runserver 0.0.0.0:$PORT