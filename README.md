## Проект:

Онлайн платформа для обучения с использованием Fast Api

**Модели:** Пользователи, Курсы, Уроки

**Идея проекта:** Разработка онлайн платформы для обучения с возможностью доступа к курсам, просмотра уроков, выполнения заданий и авторизации пользователей.

**Требования:**

- Упаковка проекта в докер-компоуз и запуск через docker compose up без дополнительной настройки
- прохождение flake8 + mypy в соответствии с конфигурациями проекта
- Кеширование всего, что возможно закешировать через redis
- Orm: sqlalchemy2.0
- Migration: alembic
- Тесты - pytest + mock на redis и rollback транзакций фикстур вместо удаления.
- Минимальные данные при разворачивании проекта (фикстуры)
- Метрики:
  - На кол-во полученных запросов в разрезе каждой ручки.
  - На кол-во ошибок по каждой ручке
  - На кол-во отправленных запросов
  - Время выполнения каждой ручки в среднем (гистограмма)
  - Время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма))
- Валидация входящих данных (pydantic)
- Настройки в env
- Без дублирования кода
- poetry как сборщик пакетов
- Обработка ошибок и соответствующие статусы ответов
- В README.md ожидается увидеть как что работает, чтобы можно было ознакомиться проще с проектом

---

**Перед запуском проекта нужно создать:**

1. `.env` в папке `/grafana`, пример:

```
GF_DATABASE_TYPE = postgres
GF_DATABASE_NAME = main_db
GF_DATABASE_USER = postgres
GF_DATABASE_PASSWORD = postgres
GF_DATABASE_HOST = web_db:5432
GF_SECURITY_ADMIN_USER = admin
GF_SECURITY_ADMIN_PASSWORD = admin
```

2. `.env` в папке `/conf`, пример:

```
BIND_PORT=8000
BIND_IP=0.0.0.0


DB_URL=postgresql+asyncpg://postgres:postgres@web_db:5432/main_db
JWT_SECRET_SALT=asdasdasdasdasdasd

KAFKA_BOOTSTRAP_SERVERS=["kafka:29092"]
KAFKA_TOPIC=test_resize_image

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minio123
MINIO_HOST=minio
MINIO_PORT=9000
```

---

Далее, чтобы запустить проект нужна команда:

```
sudo docker-compose up
```

---

**После запуска, доступно:**

| Название     | Ссылка                      |
| ------------ | --------------------------- |
| Документация | http://0.0.0.0:8000/swagger |
| Метрика      | http://0.0.0.0:8000/metrics |
| Grafana      | http://0.0.0.0:3000/login   |
| MinIO        | http://0.0.0.0:9001/login   |

---
