#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/sirius/sirius.user.json fixture/sirius/sirius.restaurant.json fixture/sirius/sirius.order.json fixture/sirius/sirius.product.json fixture/sirius/sirius.order_product.json


exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
