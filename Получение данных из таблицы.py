"""
result = User.query.<method>()
User.query.all()-возвращает результат запроса (объект Query) в виде списка
User.query.count()-возвращает общее количество записей в запросе
User.query.first()-возвращает первый результат из запроса или None, если записей нет
User.query.get(pk)-возвращает объект по первичному ключу или None, если объект не был найден
"""
import json

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
    age = db.Column(db.Integer)


db.drop_all()
db.create_all()

user_john = User(id=1, name="John", age=18)
user_kate = User(id=2, name="Kate", age=16)

# db.session.add(user_john)
# db.session.add(user_john)

users = [user_kate, user_john]
db.session.add_all(users)

print(db.session.new)  # список недобавленных моделей

db.session.commit()


@app.route("/users/first")
def get_first_user():
    user = User.query.first()

    return json.dumps({
        "id": user.id,
        "name": user.name,
        "age": user.age
    })


@app.route("/users/count")
def get_user_count():
    user_count = User.query.first()

    return json.dumps(user_count)


@app.route("/users")
def get_user_all():
    user_list = User.query.all()

    user_response = []

    for user in user_list:
        user_response.append(
            {
                "id": user.id,
                "name": user.name,
                "age": user.age
            }
        )

    return json.dumps(user_response)


@app.route("/users/<int:sid>")
def get_user_id(sid):
    user = User.query.get(sid)

    if user is None:
        return 'user not found'

    return json.dumps({
        "id": user.id,
        "name": user.name,
        "age": user.age
    })


if __name__ == "__main__":
    app.run(debug=True)
