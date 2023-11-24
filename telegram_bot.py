from telebot import *
import requests
import random

# Токен вашего телеграм-бота
BOT_TOKEN = '6553285113:AAGcCn70J3148zwU6vIR23I0unR-TvQMgsA'

# Создание экземпляра телеграм-бота
bot = telebot.TeleBot(BOT_TOKEN)

# URL вашего сервера, на который будут отправляться данные
SERVER_URL = 'http://localhost:5000/receive_data'  # Замените на реальный URL вашего сервера

# Функция для отправки данных на сервер
def send_to_server(data):
    # Отправка данных на сервер
    requests.post(SERVER_URL, json={'user_info': data})

# Функция для генерации кода
def code_generation():
    random_code = random.randint(1000, 9999)
    return f"Ваш код: {random_code}"

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    delet = telebot.types.ReplyKeyboardRemove()
    chat_id = message.chat.id

    user_info = {
        # 'chat_id': chat_id
    }

    bot.send_message(chat_id, 'Привет! Я ваш бот. Давайте знакомиться!')

    # Запрашиваем имя
    bot.send_message(chat_id, 'Введите ваше имя:', reply_markup=delet)
    bot.register_next_step_handler(message, process_name_step, user_info)

# Обработчик команды /generation
@bot.message_handler(commands=['generation'])
def generation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Генерация")

    markup.add(btn)
    bot.send_message(message.chat.id, text="Теперь Вы можете сгенерировать код", reply_markup=markup)

# Обработчик команды /choice
@bot.message_handler(commands=['choice'])
def choice(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Аудитория №1", callback_data="btn1")
    btn2 = types.InlineKeyboardButton(text="Аудитория №2", callback_data="btn2")

    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(message.chat.id, text="Выберите аудиторию", reply_markup=markup)

# Обработчик ввода имени
def process_name_step(message, user_info):
    chat_id = message.chat.id
    user_info['name'] = message.text

    # Запрашиваем фамилию
    bot.send_message(chat_id, 'Введите вашу фамилию:')
    bot.register_next_step_handler(message, process_surname_step, user_info)

# Обработчик ввода фамилии
def process_surname_step(message, user_info):
    chat_id = message.chat.id
    user_info['surname'] = message.text

    # Запрашиваем номер группы
    bot.send_message(chat_id, 'Введите номер вашей группы:')
    bot.register_next_step_handler(message, process_group_step, user_info)

# Обработчик ввода номера группы
def process_group_step(message, user_info):
    chat_id = message.chat.id
    user_info['group'] = message.text
    user_info['chat_id'] = chat_id

    # Завершаем регистрацию
    bot.send_message(chat_id, 'Спасибо за регистрацию!')

    # Отправляем данные на сервер
    send_to_server(user_info)
    generation(message)

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def get_text(message):
    if (message.text == 'Генерация'):
        choice(message)

# Обработчик инлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery):
    if call.message:
        if call.data == "btn1" or call.data == "btn2":
            bot.send_message(call.message.chat.id, code_generation())

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Успешно✅", callback_data="but_2"))
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=markup)

# Запуск бота в режиме long polling
bot.polling(none_stop=True)
