#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/sirius/sirius.user.json fixture/sirius/sirius.deal.json \
 fixture/sirius/sirius.client.json


exec uvicorn webapp.on_startup.main:create_app --host=$BIND_IP --port=$BIND_PORT
