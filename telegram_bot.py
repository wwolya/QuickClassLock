import telebot
import requests

BOT_TOKEN = '6553285113:AAGcCn70J3148zwU6vIR23I0unR-TvQMgsA'

bot = telebot.TeleBot(BOT_TOKEN)

# URL вашего сервера, на который будут отправляться данные
SERVER_URL = 'http://localhost:5000'  # Замените на реальный URL вашего сервера


def send_to_server(user_info):
    # Отправка данных на сервер
    requests.post(SERVER_URL, json={'user_info': user_info})


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    user_info = {
        #'chat_id': chat_id
        }

    bot.send_message(chat_id, 'Привет! Я ваш бот. Давайте знакомиться!')

    # Запрашиваем имя
    bot.send_message(chat_id, 'Введите ваше имя:')
    bot.register_next_step_handler(message, process_name_step, user_info)


def process_name_step(message, user_info):
    chat_id = message.chat.id
    user_info['name'] = message.text

    # Запрашиваем фамилию
    bot.send_message(chat_id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, process_surname_step, user_info)


def process_surname_step(message, user_info):
    chat_id = message.chat.id
    user_info['surname'] = message.text

    # Запрашиваем номер группы
    bot.send_message(chat_id, 'Введите номер вашей группы:')
    bot.register_next_step_handler(message, process_group_step, user_info)


def process_group_step(message, user_info):
    chat_id = message.chat.id
    user_info['group'] = message.text

    # Завершаем регистрацию
    bot.send_message(chat_id, 'Спасибо за регистрацию! Теперь вы можете отправлять сообщения.')

    # Отправляем данные на сервер
    send_to_server(user_info)


if __name__ == '__main__':
    bot.polling(none_stop=True)
