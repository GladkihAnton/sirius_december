#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/sirius/sirius.user.json fixture/sirius/sirius.institution.json \
    fixture/sirius/sirius.group.json fixture/sirius/sirius.teacher.json \
    fixture/sirius/sirius.student.json fixture/sirius/sirius.subject.json \
    fixture/sirius/sirius.group_subject.json fixture/sirius/sirius.journal.json


exec uvicorn webapp.main:create_app --host=$BIND_IP --port=$BIND_PORT
