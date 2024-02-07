#!/usr/bin/env bash

echo "Start service"

# выполняет миграции базы данных
python scripts/migrate.py

# загрузка данных из файлов в бд
python scripts/load_data.py fixture/sirius/sirius.user.json
python scripts/load_data.py fixture/sirius/sirius.employee.json
python scripts/load_data.py fixture/sirius/sirius.vacation.json

# команда говорит uvicorn взять приложение,созданное в файле main.py в пакете webapp, и запустить его на указанном хосте и порте.
exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
