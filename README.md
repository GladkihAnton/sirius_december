Онлайн платформа для обмена рецептами с использованием Fast Api
- Модели: Пользователи, Рецепты, Ингредиенты
<<<<<<< HEAD
- Платформа, где пользователи могут обмениваться рецептами блюд, делиться своим опытом приготовления и находить новые идеи для кулинарии.

Технологии проекта:
- прохождение flake8 + mypy в соответствии с конфигурациями проекта
- Кеширование через redis
- Метрики на время выполнения всех интеграционных методов (запросы в бд, редис и тп (гистограмма)

## API requests examples

### Authorization

- Register
curl -X POST http://127.0.0.1:8000/auth/register \
    -H "Content-Type: application/json" -d '{"username": "new", "password": "new"}'

- Login
curl -X POST http://127.0.0.1:8000/auth/login \
    -H "Content-Type: application/json" -d '{"username": "new user", "password": "new"}'

- Info 
curl -X POST http://127.0.0.1:8000/auth/info

- Delete
curl -X POST http://127.0.0.1:8000/auth/delete_user/1 \
    -H "Authorization: Bearer ACCESS_TOKEN"

- Update
curl -X POST http://127.0.0.1:8000/auth/update_user/1 \
    -H "Content-Type: application/json" -d '{"username": "new", "password": "new"}'


### Ingredient

- Create
curl -X POST http://127.0.0.1:8000/ingredient/create \
    -H "Content-Type: application/json" -d '{"title": "new ingredient"}'

- Read
curl -X GET http://127.0.0.1:8000/ingredient/read \
    -H "Content-Type: application/json" -d '{"title": "new ingredient"}'

- Update
curl -X POST http://127.0.0.1:8000/ingredient/update/1 \
     -H "Content-Type: application/json" -d '{"title": "newt"}'

- Delete
curl -X POST http://127.0.0.1:8000/ingredient/delete/1 \
    -H "Content-Type: application/json"

- Read all
curl -X GET http://127.0.0.1:8000/ingredient/read_all \
    -H "Content-Type: application/json"


### Recipe

- Create
curl -X POST http://127.0.0.1:8000/recipe/create \
    -H "Content-Type: application/json" \
    -d '{"title": "new recip", "ingredients": ["Water", "Pasta"]}'

- Read
curl -X GET http://127.0.0.1:8000/recipe/read \
    -H "Content-Type: application/json" -d '{"title": "new recipe"}'

- Update
curl -X POST http://127.0.0.1:8000/recipe/update/1 \
    -H "Content-Type: application/json" -d '{"title": "newt"}'

- Add ingredient
curl -X POST http://127.0.0.1:8000/recipe/add_ingredient/1 \
    -H "Content-Type: application/json" -d '{"ingredient": "Water"}'

- Delete
curl -X POST http://127.0.0.1:8000/recipe/delete/1 \
    -H "Content-Type: application/json"

- Read all
curl -X GET http://127.0.0.1:8000/recipe/read_all \
    -H "Content-Type: application/json"
=======
- Идея проекта: Создание платформы, где пользователи могут обмениваться рецептами блюд, делиться своим опытом приготовления и находить новые идеи для кулинарии.

# API requests examples

## auth

> REGISTER
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username": "new user", "password": "new"}'


> LOGIN
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username": "new user", "password": "new"}'


> INFO 
curl -X POST http://127.0.0.1:8000/auth/info


> DELETE
curl -X POST http://127.0.0.1:8000/auth/delete_user/1 \
    -H "Authorization: Bearer ACCESS_TOKEN"


> UPDATE
curl -X POST http://127.0.0.1:8000/auth/update_user/1 -H "Content-Type: application/json" -d '{"username": "new", "password": "new"}'


## INGREDIENT

> CREATE
curl -X POST http://127.0.0.1:8000/ingredient/create -H "Content-Type: application/json" -d '{"title": "new ingredient"}'


> READ
curl -X GET http://127.0.0.1:8000/ingredient/read -H "Content-Type: application/json" -d '{"title": "new ingredient"}'


> UPDATE
curl -X POST http://127.0.0.1:8000/ingredient/update/1 -H "Content-Type: application/json" -d '{"title": "newt"}'


> DELETE
curl -X POST http://127.0.0.1:8000/ingredient/delete/1 -H "Content-Type: application/json"


> READ_ALL
curl -X GET http://127.0.0.1:8000/ingredient/read_all    -H "Content-Type: application/json"


## RECIPE

> CREATE
curl -X POST http://127.0.0.1:8000/recipe/create -H "Content-Type: application/json" -d '{"title": "new recip", "ingredients": ["Water", "Pasta"]}'


> READ
curl -X GET http://127.0.0.1:8000/recipe/read -H "Content-Type: application/json" -d '{"title": "new recipe"}'


> UPDATE
curl -X POST http://127.0.0.1:8000/recipe/update/1 -H "Content-Type: application/json" -d '{"title": "newt"}'


> ADD INGREDIENT
curl -X POST http://127.0.0.1:8000/recipe/add_ingredient/1 -H "Content-Type: application/json" -d '{"ingredient": "Water"}'


> DELETE
curl -X POST http://127.0.0.1:8000/recipe/delete/1 -H "Content-Type: application/json"


> READ_ALL
curl -X GET http://127.0.0.1:8000/recipe/read_all    -H "Content-Type: application/json"


