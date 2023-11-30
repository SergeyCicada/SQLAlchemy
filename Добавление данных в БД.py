"""
1. Создать объект
2. Добавить его в сессию db.session.add() or db.session.add_all()-передаем переменную в виде списка
3. Выполнить коммит db.session.commit()
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Подключение к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение уведомлений
app.app_context().push()  # CONTEXT FOR SQLALCHEMY

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.integer)


db.drop_all()
db.create_all()

user_john = User(id=1, name="John", age=18)
user_kate = User(id=2, name="Kate", age=16)

# db.session.add(user_john)
# db.session.add(user_john)

users = [user_kate, user_john]
db.session.ass_all(users)

print(db.session.new)  # список недобавленных моделей

db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
