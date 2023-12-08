#!/usr/bin/env bash

echo "Start service"
exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
