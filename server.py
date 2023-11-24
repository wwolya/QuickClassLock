from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Создание Flask-приложения
app = Flask(__name__)

# Конфигурация базы данных (используется SQLite в данном случае)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Определение модели RegisteredUsers для таблицы зарегистрированных пользователей
class RegisteredUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    group = db.Column(db.String(20), nullable=False)
    chat_id = db.Column(db.String(50), nullable=False)
    access_logs = db.relationship('AccessLog', backref='user', lazy=True)

# Определение модели AccessLog для таблицы журнала доступа
class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('registered_users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lock_opened = db.Column(db.Boolean, nullable=False)

# Маршрут для отображения главной страницы
@app.route('/')
def main_page():
    return render_template('main.html')

# Маршрут для отображения списка пользователей
@app.route('/user_list')
def user_list():
    users = RegisteredUsers.query.all()
    return render_template('user_list.html', users=users, access_logs=None)

# Маршрут для отображения журнала доступа
@app.route('/access_log')
def access_log():
    access_logs = AccessLog.query.all()
    return render_template('access_log.html', access_logs=access_logs)

# Маршрут для приема данных от телеграм-бота (регистрация нового пользователя и создание записи в журнале доступа)
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    # Извлечение данных о пользователе из JSON-запроса
    name = data['user_info'].get('name')
    surname = data['user_info'].get('surname')
    group = data['user_info'].get('group')
    chat_id = data['user_info'].get('chat_id')

    # Создание нового пользователя и записи в журнале доступа
    new_user = RegisteredUsers(name=name, surname=surname, group=group, chat_id=chat_id)
    db.session.add(new_user)
    db.session.commit()

    new_access_log = AccessLog(user_id=new_user.id, timestamp=datetime.utcnow(), lock_opened=False)
    db.session.add(new_access_log)
    db.session.commit()

    return jsonify({'status': 'success', 'new_user_id': new_user.id, 'new_access_log_id': new_access_log.id})

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        # Создание всех таблиц базы данных при запуске приложения
        db.create_all()
    app.run(debug=True)