"""
relationship - дополнительное распознование связи - автоматически подгружает в виде объектов, чтобы мы могли
общаться к полям объекта сразу, без дополнительных запросов
"""
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'  # Подключение к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение уведомлений
app.app_context().push()  # CONTEXT FOR SQLALCHEMY

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    group = relationship("Group")


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    users = relationship("User")


db.drop_all()
db.create_all()


group_01 = Group(id=1, name="Group_01")
user_01 = User(id=1, name="Sergey", age=31, group=group_01)  # мы прокидывает в group объект group_01

db.session.add(user_01)
db.session.add(group_01)

user_02 = User(id=2, name="Mixa", age=35)
group_02 = Group(id=2, name="Group_02", users=[user_02])  # можем передать несколько объектов списком

db.session.add(user_01)
db.session.add(group_02)
db.session.commit()


user_with_group = User.query.get(1)
print(user_with_group.group.name)

if __name__ == "__main__":
    app.run(debug=True)