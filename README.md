Онлайн сервис бронирования туров с использованием Fast Api
   - Модели: Пользователи, Туры, Бронирования
   - Идея проекта: Разработка онлайн сервиса для бронирования туров с возможностью просмотра доступных туров, выбора даты, оформления бронирования и авторизации пользователей.

Требования к проекту:
- [x] Упаковка проекта в докер-компоуз и запуск через docker compose up без дополнительной настройки
- [x] Прохождение flake8 + mypy в соответствии с конфигурациями проекта
- [x] Кеширование всего, что возможно закешировать через redis
- [x] Orm:  sqlalchemy2.0
- [ ] Migration: alembic
- [x] Тесты - pytest + mock на redis и rollback транзакций фикстур вместо удаления.
- [x] Минимальные данные при разворачивании проекта (фикстуры)
- [x] Метрики: 
  - [x] На кол-во полученных запросов в разрезе каждой ручки.
  - [x] На кол-во ошибок по каждой ручке
  - [x] На кол-во отправленных запросов
  - [x] Время выполнения каждой ручки в среднем (гистограмма)
  - [x] Время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма)
- [x] Валидация входящих данных (pydantic)
- [x] Настройки в env
- [x] Без дублирования кода
- [x] poetry как сборщик пакетов
- [x] Обработка ошибок и соответствующие статусы ответов
- [x] В README.md ожидается увидеть как что работает, чтобы можно было ознакомиться проще с проектов

# Run
  
    git clone https://github.com/kirillsev1/FastAPI_resize_img.git
    
    cd FastAPI_resize_img

    git checkout feature/prixodko_kirill

    docker compose up --build

# API

## auth
`/registration` - creates new user / returns 409 - conflict if user already exists 

>   curl -X POST http://127.0.0.1:8000/auth/register \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test1",
        "password": "test"
    }' 

`auth/token` - returns jwt token for auth

>   curl -X POST http://127.0.0.1:8000/auth/token \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test1",
        "password": "test"
    }' 

`auth/info` - returns user creds from jwt token

>   curl -X POST http://127.0.0.1:8000/auth/info \
    -H "Authorization: Bearer ACCESS_TOKEN"

## crud
`/user/{user_id}` - removes user by id

>   curl -X DELETE http://127.0.0.1:8000/api/v1/user/{user_id} \
    -H "Authorization: Bearer ACCESS_TOKEN"

`/user/{user_id}`(Redis usage) - returns user by id

>   curl -X GET http://127.0.0.1:8000/api/v1/user/{user_id} \
    -H "Authorization: Bearer ACCESS_TOKEN"

`/user/page/{page_id}` - returns users using offset

>   curl -X GET http://127.0.0.1:8000/api/v1/user/page/{page_id} \
    -H "Authorization: Bearer ACCESS_TOKEN"

`/user/{user_id}` - updates user creds

>   curl -X PUT http://127.0.0.1:8000/user/{user_id} \
    -H "Content-Type: application/json" \
    -d '{
        "username": "test45",
        "password": "test"
    }' 

> **NOTE**
> 
> The same situation with tour/review/reservation/activity models but creation locates on `/{model_name}/`

# Pytest
## Fixtures
#### `scope='session'`

 - app - creates FastAPI application
 - event_loop - returns AbstractEventLoop
 - **_migrate_db** - global fixture for all db tables, after all tests will complete it will create empty tables or drop all of them

#### `scope='function'`

 - **client** - returns AsyncClient
 - **db_session** - creates database session and after tests rollbacks connection
 - **_load_fixtures** - loads all accepted model fixtures to session
 - **_mock_redis** - mocking redis
 - **access_token** - returns access_token for tests with auth
 - **_common_api_fixture** - uses load_fixtures
 - **_common_api_with_redis_fixture** - uses load_fixtures and mock_redis

## Mock


> **TestRedisClient** - redis mocking class. Uses class methods to add and get data by key


# Docker compose
## App - web
> Container with FastAPI application 

## DB - web_db
> ![Schema](README_source/schema.png)

## Redis - redis
> 1. **get_cache_title** - creates redis key in this way:
>    - **{settings.REDIS_SIRIUS_CACHE_PREFIX}:{model}:{model_id}**
>    - **settings.REDIS_SIRIUS_CACHE_PREFIX** - for example db schema name
>    - **model** - db model name
>    - **model_id** - db model id
> 
> 
> 2. **redis_set** - sets data to redis
>
> 
> 3. **redis_get** - gets data from redis
>
> 
> 4. **get_redis** - returns redis object

## Prometheus - prometheus
### Metrics
> **REQUEST_COUNT** - 
> The http_requests_total metric tracks the total count of HTTP requests, categorized by method, endpoint, and http_status.
> 
> **query**: sum(http_requests_total) by (method, endpoint, http_status)

> **ERROR_COUNT** -
> The http_errors_total metric keeps track of the total count of HTTP errors, categorized by method, endpoint, and http_status.
>
> **query**: sum(http_errors_total) by (method, endpoint, http_status)

> **INTEGRATIONS_LATENCY** -
> The sirius_integrations_latency_seconds metric represents the latency of integrations, categorized by integration name.
>
> **query**: histogram_quantile(0.99, sum(rate(sirius_integrations_latency_seconds_bucket[1m])) by (le, integration))

> **ROUTES_LATENCY** -
> The sirius_routes_latency_seconds metric tracks the latency of routes, categorized by method and endpoint.
>
> **query**: histogram_quantile(0.99, sum(rate(sirius_routes_latency_seconds_bucket[1m])) by (le, method, endpoint))

## Grafana - grafana
> ### Metrics
> ![Metrics Dashboard](README_source/grafana.jpg)

# .env/.env.example
> BIND_PORT=8000
> BIND_IP=0.0.0.0
>    
>    
>    DB_URL=postgresql+asyncpg://postgres:postgres@web_db:5432/main_db
>    JWT_SECRET_SALT=asdasdasdasdasdasd
>    
>    REDIS_HOST=redis
>    REDIS_PORT=6379
>    REDIS_PASSWORD=
>    
>    REDIS_SIRIUS_CACHE_PREFIX=sirius
