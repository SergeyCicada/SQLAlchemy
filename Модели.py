"""Валидная модель
1. Нужно наследоваться от базового класса db.Model.
2. Необходимо объявить имя таблицы с помощью атрибута
__tablename__
3. Должна быть как минимум одна колонка которая является частью первичного ключа

Создание всех таблиц
db.create_all()

Удалить таблицы
db.drop_all()"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Подключение к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # Отключение уведомлений
app.app_context().push()  # CONTEXT FOR SQLALCHEMY

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.integer)


db.create_all()

user_john = User(id=1, name="John", age=18)
user_kate = User(id=2, name="Kate", age=16)

if __name__ == "__main__":
    app.run(debug=True)