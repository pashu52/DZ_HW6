from fastapi import FastAPI
from routers import users, products, orders

# Создание экземпляра FastAPI приложения
app = FastAPI()

# Включение маршрутов из модулей users, products и orders в приложение
app.include_router(users.router)  # Включение маршрутов пользователей
app.include_router(products.router)  # Включение маршрутов продуктов
app.include_router(orders.router)  # Включение маршрутов заказов

# Проверка, является ли текущий файл главным скриптом
if __name__ == "__main__":
    import uvicorn

    # Запуск сервера с помощью Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
