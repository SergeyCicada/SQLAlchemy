from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc, func
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Подключение к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение уведомлений
app.app_context().push()  # CONTEXT FOR SQLALCHEMY

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # Уникальный первичный ключ
    passport_number = db.Column(db.String(3), unique=True)  # Уникальна, но не является частью первичного ключа
    name = db.Column(db.String(100), nullable=False)  # Запрет пустых колонок
    age = db.Column(db.Integer, db.CheckConstraint("age > 18"))  # Ограничения на возраст или другое условие
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))  # Связь с другой таблицей

    group = relationship("Group")


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = relationship("User")



db.create_all()


group_01 = Group(id=1, name="Group_01")
group_02 = Group(id=2, name="Group_02")

user_01 = User(id=1, name="Sergey", age=31, group=group_01)
user_02 = User(id=2, name="Max", age=46, group=group_01)
user_03 = User(id=3, name="Andy", age=21, group=group_01)
user_04 = User(id=4, name="Sandy", age=20, group=group_02)
user_05 = User(id=5, name="Harry", age=71, group=group_02)
user_06 = User(id=6, name="Ron", age=54, group=group_02)

db.session.add_all([user_01, user_02, user_03, user_04, user_05, user_06])
db.session.commit()

"""Запросы на обновление данных"""

user = User.query.get(2)
print(user.name)

user.name = "Update name"
db.session.add(user)  # добавление измененного пользователя
db.session.commit()

user = User.query.get(2)
print(user.name)