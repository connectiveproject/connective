release: cd server && python manage.py migrateweb: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorkerworker: celery worker --app=config.celery_app --loglevel=info
beat: cd server && celery beat --app=config.celery_app --loglevel=info
