from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Словарь для хранения информации о пользователях
user_info = {
    1: {'name': 'Иван', 'surname': 'Иванов', 'group': 'Группа 1', 'chat_id':'123'},
    2: {'name': 'Петр', 'surname': 'Петров', 'group': 'Группа 2','chat_id': '345'},
}

@app.route('/', methods=['POST'])
def receive_data():
    data = request.json

    name = data['user_info'].get('name')
    surname = data['user_info'].get('surname')
    group = data['user_info'].get('group')
    chat_id = data['user_info'].get('chat_id')

    new_user_id = max(user_info.keys()) + 1
    user_info[new_user_id] = {'name': name, 'surname': surname, 'group': group, 'chat_id':chat_id}

    return jsonify({'status': 'success', 'new_user_id': new_user_id})

@app.route('/')
def index():
    return render_template('user_list.html', users=user_info)

if __name__ == '__main__':
    app.run(debug=True)