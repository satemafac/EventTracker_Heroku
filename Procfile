web: gunicorn Event_Tracker.wsgi:application --chdir Event_Tracker --log-level debug --log-file -
runserver: cd Event_Tracker && python manage.py runserver 0.0.0.0:$PORT
release: python Event_Tracker/manage.py migrate