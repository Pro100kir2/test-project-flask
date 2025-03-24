from app import db
from app.models.user import User
from flask import flash
from datetime import datetime


class UserService:
    @staticmethod
    def register_user(name, password, birth_date, gender, full_name):
        """Регистрация нового пользователя"""
        # Проверка возраста
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        age = (datetime.today().date() - birth_date).days // 365
        if age > 100:
            flash("Возраст не должен превышать 100 лет", 'error')
            return None

        # Создаем пользователя
        user = User(name=name, password=password, birth_date=birth_date, gender=gender, full_name=full_name)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def check_user_credentials(self, name, password):
        # Логика для проверки данных при входе
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            return "Success"
        return "Invalid credentials"

    @staticmethod
    def get_all_users():
        """Получение всех пользователей"""
        users = User.query.all()
        return users

    @staticmethod
    def get_user_by_name(name):
        """Получение пользователя по имени"""
        user = User.query.filter_by(name=name).first()
        return user
