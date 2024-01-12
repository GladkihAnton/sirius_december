#!/usr/bin/env bash

echo "Start service"

python scripts/migrate.py

python scripts/load_data.py fixture/tms/tms.user.json fixture/tms/tms.category.json fixture/tms/tms.task.json

exec uvicorn webapp.on_startup.main:create_app --host=$BIND_HOST --port=$BIND_PORT