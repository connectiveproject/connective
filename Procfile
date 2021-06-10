release: cd server && python manage.py migrate
web: cd server && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
worker: cd server && celery worker --app=config.celery_app --loglevel=info
beat: cd server && celery beat --app=config.celery_app --loglevel=info
