rm -rf /frontend/build/* && cp -r /frontend_tmp/build/* /frontend/build
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
gunicorn -w 4 -b 0.0.0.0:8000 project.wsgi:application
# python manage.py runserver 0:8000