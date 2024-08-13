web: gunicorn Event_Tracker.wsgi:application --chdir Event_Tracker --log-level debug --log-file -
release: python Event_Tracker/manage.py migrate