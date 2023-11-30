"""
result = User.query.<method>()

User.query.filter(*criterion)
Возвращает экземпляр Query после применения оператора WHERE

User.query.limit(limit)
Возвращает экземпляр Query после применения оператора LIMIT

User.query.offset(offset)
Возвращает экземпляр Query после применения оператора OFFSET

User.query.order_by (*criterion)
Возвращает экземпляр Query после применения оператора ORDER BY

User.query.join(*props)
Возвращает экземпляр Query после создания SQL INNER JOIN

User.query.group_by(*criterion)
Возвращает экземпляр Query после добавления оператора GROUP BY

"""


import json

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

"""SQL -> WHERE"""
query = db.session.query(User).filter(User.name == "Max")
print(f"Запрос: {query}")
print(f"Результат: {query.first().name}")


"""SQL -> WHERE(Required record)"""
query = db.session.query(User).filter(User.name == "Max")
print(f"Запрос: {query}")
print(f"Результат: {query.one()}")  # .one - выбрасывает полноценную ошибку для обработки при отстуствии резальтата

"""SQL -> WHERE... AND"""
query = db.session.query(User).filter(User.id <= 5, User.age > 20)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> LIKE"""
query = db.session.query(User).filter(User.name.like("M%"))
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> WHERE... OR"""
query = db.session.query(User).filter(
    or_(User.id <= 5, User.age > 20)
)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> IS NULL"""
query = db.session.query(User).filter(User.passport_number == None) # обяательно используем ==, а не is None
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> IS NOT NULL"""
query = db.session.query(User).filter(User.passport_number != None)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> WHERE... IN - вхождение каких либо значений"""
query = db.session.query(User).filter(User.id.in_([1, 2]))
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> WHERE... NOT IN"""
query = db.session.query(User).filter(User.id.notin_([1, 2]))
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> WHERE... BETWEEN"""
query = db.session.query(User).filter(User.id.between(1, 6))
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> LIMIT"""
query = db.session.query(User).limit(2)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> LIMIT OFFSET"""
query = db.session.query(User).limit(2).offset(2)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> ORDER BY"""
query = db.session.query(User).order_by(User.id)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")
query = db.session.query(User).order_by(desc(User.id))
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> INNER JOIN"""
query = db.session.query(User.name, Group.name).join(Group)
print(f"Запрос: {query}")
print(f"Результат: {query.all()}")

"""SQL -> GROUP BY"""
query = db.session.query(func.count(User.id)).join(Group).filter(Group.id == 1).group_by(Group.id)
print(f"Запрос: {query}")
print(f"Результат: {query.scalar()}")

if __name__ == "__main__":
    app.run(debug=True)
    