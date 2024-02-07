Онлайн платформа для обмена товаров с использованием Fast Api
- Модели: Пользователи, Товары, Обмены
- Идея проекта: Разработка онлайн платформы для обмена товаров между пользователями с возможностью создания объявлений, оформления обменов и авторизации пользователей.

# Requests to API

## User Authenticate

> Sign up

```
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{"username": "test_name", "password": "test_password"}'
```

> Sign in

```
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d '{"username": "test_name", "password": "test_password"}'
```

> Information

```
curl -X POST http://127.0.0.1:8000/auth/info -H "Authorization: Bearer ACCESS_TOKEN"
```

> Update

```
curl -X POST http://127.0.0.1:8000/auth/update_user/1 -H "Content-Type: application/json" -d '{"username": "new_name", "password": "new_password"}'
```

> Delete

```
curl -X POST http://127.0.0.1:8000/auth/delete_user/1 -H "Authorization: Bearer ACCESS_TOKEN"
```


## API Requests 'Items'

> Create

```
curl -X POST http://127.0.0.1:8000/item/create -H "Content-Type: application/json" -d '{"name": "new item"}'
```

> Read

```
curl -X GET http://127.0.0.1:8000/item/read -H "Content-Type: application/json" -d '{"name": "new item"}'
```

> Read all

```
curl -X GET http://127.0.0.1:8000/item/read_all -H "Content-Type: application/json"
```

> Update

```
curl -X POST http://127.0.0.1:8000/item/update/1 -H "Content-Type: application/json" -d '{"name": "newer item"}'
```

> Delete

```
curl -X POST http://127.0.0.1:8000/item/delete/1 -H "Content-Type: application/json"
```



## API Requests 'Exchanges'

> Create

```
curl -X POST http://127.0.0.1:8000/exchange/create -H "Content-Type: application/json" -d '{"item1_id": 1, "item2_id": 2}'
```

> Read

```
curl -X GET http://127.0.0.1:8000/exchange/read/1 -H "Content-Type: application/json"
```

> Read all

```
curl -X GET http://127.0.0.1:8000/exchange/read_all -H "Content-Type: application/json"
```

> Update

```
curl -X POST http://127.0.0.1:8000/exchange/update/1 -H "Content-Type: application/json" -d '{"item1_id": 3, "item2_id": 4}'
```

> Delete

```
curl -X POST http://127.0.0.1:8000/exchange/delete/1 -H "Content-Type: application/json"
```


