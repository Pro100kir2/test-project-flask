from flask import flash, Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.services.user_service import UserService
from datetime import datetime
import re

# Blueprint для контроллера пользователей
user_controller = Blueprint('user_controller', __name__)

# Главная страница
@user_controller.route('/', methods=['GET'])
def index():
    """Главная страница"""
    if 'user_id' in session:
        return render_template('index.html', is_authenticated=True)
    return render_template('index.html', is_authenticated=False)

@user_controller.route('/registration', methods=['GET', 'POST'])
def registration_page():
    """Страница регистрации и обработка формы"""
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        birth_date = request.form.get('birth_date')
        gender = request.form.get('gender')
        full_name = request.form.get('full_name')

        # Печать введенных данных в консоль
        print(f"Введенные данные: Имя: {name}, Пароль: {password}, Дата рождения: {birth_date}, Пол: {gender}, Полное имя: {full_name}")

        # Валидация имени
        if len(name) < 8 or len(name) > 12:
            flash("Имя должно быть от 8 до 12 символов")
            return render_template('register.html', name=name, birth_date=birth_date, gender=gender, full_name=full_name)

        # Проверка на латинские буквы и цифры в имени
        if not re.match("^[a-zA-Z0-9]+$", name):
            flash("Имя должно содержать только латинские буквы и цифры")
            return render_template('register.html', name=name, birth_date=birth_date, gender=gender, full_name=full_name)

        # Валидация пароля
        if len(password) < 8 or len(password) > 12:
            flash("Пароль должен быть от 8 до 12 символов")
            return render_template('register.html', name=name, birth_date=birth_date, gender=gender, full_name=full_name)

        # Преобразование даты в нужный формат и проверка возраста
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()

            # Проверка возраста
            age = (datetime.today().date() - birth_date_obj).days // 365
            if age > 100:
                flash("Возраст не может быть больше 100 лет")
                return render_template('register.html', name=name, birth_date=birth_date, gender=gender,
                                       full_name=full_name)
        except Exception as e:
            print(f"Ошибка преобразования даты: {e}")
            flash("Неверный формат даты. Используйте формат YYYY-MM-DD.")
            return render_template('register.html', name=name, birth_date=birth_date, gender=gender,
                                   full_name=full_name)

        # Создание пользователя
        user = UserService.register_user(name, password, birth_date, gender, full_name)
        if user:
            flash("Регистрация прошла успешно! Теперь войдите.")
            return redirect(url_for('user_controller.login_page'))
        else:
            flash("Имя пользователя уже занято")
            return render_template('register.html', name=name, birth_date=birth_date, gender=gender, full_name=full_name)

    return render_template('register.html')

# Страница входа
@user_controller.route('/login', methods=['GET', 'POST'])
def login_page():
    """Страница входа и авторизация"""
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = UserService.get_user_by_name(name)

        if user and user.password == password:
            session['user_id'] = user.id
            flash("Успешный вход!")
            return redirect(url_for('user_controller.index'))
        else:
            flash("Неверное имя пользователя или пароль")
            return render_template('login.html')

    return render_template('login.html')


# Страница вывода всех пользователей
@user_controller.route('/get_users', methods=['GET'])
def get_users_page():
    """Получение списка пользователей и отображение их на странице"""
    users = UserService.get_all_users()
    is_authenticated = 'user_id' in session
    return render_template('users.html', users=users, is_authenticated=is_authenticated)

# Выход из системы через веб
@user_controller.route('/logout', methods=['GET'])
def logout():
    """Завершение сессии (выход из системы)"""
    session.pop('user_id', None)  # Удаляем user_id из сессии
    flash("Вы успешно вышли из системы.")
    return redirect(url_for('user_controller.index'))

# API: Возвращает список пользователей
@user_controller.route('/api/get_users', methods=['GET'])
def get_users_api():
    """Возвращает список пользователей (API)"""
    if 'user_id' not in session:
        users = UserService.get_all_users()
        users_data = [{"name": user.name} for user in users]
    else:
        users = UserService.get_all_users()
        users_data = [{"id": user.id, "name": user.name, "password": user.password,
                       "birth_date": user.birth_date.strftime('%d.%m.%Y'), "full_name": user.full_name,
                       "gender": user.gender} for user in users]
    return jsonify(users_data)

# API: Авторизация пользователя
@user_controller.route('/api/login_user', methods=['POST'])
def login_user():
    """Авторизация пользователя (API)"""
    name = request.json.get('name')
    password = request.json.get('password')
    user = UserService.get_user_by_name(name)
    if user and user.password == password:
        session['user_id'] = user.id
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials"}), 400


# API: Регистрация пользователя
@user_controller.route('/api/register_user', methods=['POST'])
def register_user():
    """Регистрация пользователя (API)"""
    name = request.json.get('name')
    password = request.json.get('password')
    birth_date = request.json.get('birth_date')
    gender = request.json.get('gender')
    full_name = request.json.get('full_name')

    # Проверка имени пользователя (должно содержать только латинские буквы и цифры)
    if not re.match(r'^[A-Za-z0-9]+$', name):
        return jsonify({"message": "Username must contain only Latin letters and digits."}), 400

    # Проверка пароля (должен быть длиной от 8 до 12 символов)
    if not (8 <= len(password) <= 12):
        return jsonify({"message": "Password must be between 8 and 12 characters."}), 400

    # Проверка возраста (дата рождения, возраст меньше 100 лет)
    try:
        birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
        age = (datetime.now().date() - birth_date_obj).days // 365
        if age >= 100:
            return jsonify({"message": "Age must be less than 100 years."}), 400
    except ValueError:
        return jsonify({"message": "Invalid birth date format. Use 'YYYY-MM-DD'."}), 400

    # Создание пользователя
    user = UserService.register_user(name, password, birth_date, gender, full_name)
    if user:
        return jsonify({"message": "User registered successfully!"}), 201
    return jsonify({"message": "Failed to register user"}), 400

# API: Выход из системы
@user_controller.route('/api/logout', methods=['POST'])
def api_logout():
    """Завершение сессии через API (выход из системы)"""
    session.pop('user_id', None)  # Удаляем user_id из сессии
    return jsonify({"message": "Logged out successfully!"}), 200
