### Тема: Система управления медицинской клиникой

#### ENV файл
- BIND_IP: str
- BIND_PORT: int
- DB_URL: str
- JWT_SECRET_SALT: str

- REDIS_HOST: str
- REDIS_PORT: int
- REDIS_PASSWORD: str

### для каждой модели в webapp/{model_name}_api есть crud методы, а так же:

- **webapp/doctor_api/service_relation** для работы с сущностями докторов и услуг
- **webapp/patient_api/timetable_relation** для осуществления работы с записями на прием и получения данных о свободном времени
- **webapp/access** для авторизации пользователей и смены пароля 

**Таблицы**
- Doctor (specialization, first_name, last_name)
- User (username, first_name, last_name, hashed_password)
- Service (name, duration)
- Timetable (doctor_id, user_id, service_id, start, end)