release: python manage.py migrateweb: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorkerworker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
