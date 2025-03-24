from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'test_flask'

    id = db.Column(db.String(8), primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(12), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('man', 'woman', 'other'), nullable=False)
    full_name = db.Column(db.String(24), nullable=False)

    def __init__(self, name, password, birth_date, gender, full_name):
        self.id = self.generate_id()
        self.name = name
        self.password = password
        self.birth_date = birth_date
        self.gender = gender
        self.full_name = full_name

    def generate_id(self):
        """Генерация уникального ID из 8 символов (цифры + латиница)"""
        from random import choice
        from string import ascii_letters, digits
        return ''.join(choice(ascii_letters + digits) for _ in range(8))

    def __repr__(self):
        return f"<User(name={self.name}, full_name={self.full_name})>"
