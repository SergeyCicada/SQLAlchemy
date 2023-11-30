"""Основной смысл ORM

Не требуется ручного маппинга
Не надо писать запросы
Безопасность
Абстрагирование от реализации СУБД

SQLAlchemy

1. pip install"""

from flask import Flask, request, current_app
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Подключение к БД
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # Отключение уведомлений
app.app_context().push()  # CONTEXT FOR SQLALCHEMY

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)
