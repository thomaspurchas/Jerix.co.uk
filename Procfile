web: newrelic-admin run-program python jerix.co.uk/eso/manage.py run_gunicorn -b 0.0.0.0:$PORT -k gevent -w 9

worker: python jerix.co.uk/eso/manage.py celeryd -l INFO