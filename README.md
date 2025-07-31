# vacantist-bot_ashab

## Команды
Запустить туннель на нужный порт:
```
ngrok http 5050
```
Запуск приложения
```
 uvicorn app.main:app --port 5050       
```
Создания миграции
```
alembic revision --autogenerate -m "Initial revision"
```