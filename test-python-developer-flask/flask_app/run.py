from app import create_app
from app.routes import register_routes

# Создаем приложение
app = create_app()

# Регистрируем маршруты
register_routes(app)

# Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
