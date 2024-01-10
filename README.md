Онлайн платформа для обмена рецептами с использованием Fast Api
- Модели: Пользователи, Рецепты, Ингредиенты
- Идея проекта: Создание платформы, где пользователи могут обмениваться рецептами блюд, делиться своим опытом приготовления и находить новые идеи для кулинарии.

# API requests examples

## auth

> REGISTER
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'


> LOGIN
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username": "test", "password": "test"}'


> INFO 
curl -X POST http://127.0.0.1:8000/auth/info \
    -H "Authorization: Bearer ACCESS_TOKEN"


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


> GET_ALL
curl -X GET http://127.0.0.1:8000/ingredient/read_all    -H "Content-Type: application/json"

