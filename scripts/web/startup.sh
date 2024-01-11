#!/usr/bin/env bash
# startup.sh выполняет необходимые подготовительные действия и запускает сервер для обработки запросов.

echo "Start service" # выводит сообщения 

# migrate database
# python scripts/migrate.py # скрипт выполняет миграции базы данных

# Выполнение миграций Alembic
alembic upgrade head
# load fixtures

python scripts/load_data.py fixture/sirius/sirius.user.json
python scripts/load_data.py fixture/sirius/sirius.post.json
python scripts/load_data.py fixture/sirius/sirius.comment.json
# скрипт загружает тестовые данные в базу данных из файла fixture/sirius/sirius.user.json.

#  выполняется команда 
exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT

# которая запускает сервер uvicorn с приложением, созданным в файле main.py