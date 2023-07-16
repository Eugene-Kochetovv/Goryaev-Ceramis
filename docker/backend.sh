#!/bin/bash

cd fastapi_backend

alembic upgrade head

cd src

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --preload --bind=0.0.0.0:8000
