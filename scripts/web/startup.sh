#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/sirius/sirius.user.json


exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
