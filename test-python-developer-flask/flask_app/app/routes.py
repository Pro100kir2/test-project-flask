from flask import render_template, request, redirect, url_for, session
from app.controllers.user_controller import user_controller

def register_routes(app):
    """Регистрируем все маршруты для приложения."""
    app.register_blueprint(user_controller)

    @app.route('/')
    def index():
        """Главная страница, проверка на авторизацию"""
        if 'user_id' in session:
            return render_template('index.html', is_logged_in=True)
        return render_template('index.html', is_logged_in=False)

    @app.route('/registration', methods=['GET', 'POST'])
    def register_user():
        """Страница регистрации"""
        if request.method == 'POST':
            # Получаем данные из формы
            name = request.form['name']
            password = request.form['password']
            birth_date = request.form['birth_date']
            gender = request.form['gender']
            full_name = request.form['full_name']

            # Логика регистрации
            user = UserService.register_user(name, password, birth_date, gender, full_name)
            if user:
                return redirect(url_for('login_user'))  # Перенаправление на страницу логина после успешной регистрации
            return render_template('register.html', message="Ошибка регистрации")

        return render_template('register.html', message="")

    @app.route('/login', methods=['GET', 'POST'])
    def login_user():
        """Страница авторизации"""
        if request.method == 'POST':
            # Получаем данные из формы
            name = request.form['name']
            password = request.form['password']

            # Логика входа
            user = UserService.get_user_by_name(name)
            if user and user.password == password:
                session['user_id'] = user.id  # Сохраняем ID пользователя в сессии
                return redirect(url_for('index'))  # Перенаправляем на главную страницу после входа

            return render_template('login.html', message="Неверные данные для входа")

        return render_template('login.html', message="")

    @app.route('/get_users')
    def get_users():
        """Получение списка пользователей"""
        if 'user_id' not in session:
            return redirect(url_for('login_user'))  # Перенаправление на страницу логина, если не авторизован

        users = UserService.get_all_users()  # Получаем всех пользователей
        return render_template('users.html', users=users)
