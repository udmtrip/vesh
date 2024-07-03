import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('id')

score1 = 600
score2 = 800
score3 = 1000
score4 = 1200

number_of_solutions1 = 0
number_of_solutions2 = 0
number_of_solutions3 = 0
number_of_solutions4 = 0

# описание самих команд делается в BotFather

@bot.message_handler(commands=['start'])
def start_func(message):
    bot.send_message(message.chat.id, """Придумайте себе никнейм, который будет отображаться в рейтинге. 
    Оскорбительные будут забанены, использовать имена и фамилии можно, но необязательно.
    Для перезаписи используйте /nick.
    Если вы уже создавали ник, и нет необходимости создавать новый, нажмите НАЗАД.)""")
    bot.register_next_step_handler(message, registration)

def registration(message):

    user_id = message.from_user
    user_name = message.text

    connection = sqlite3.connect('results.sql')
    cur = connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Competitors(user_id INTENGER PRIMARY KEY, user_name TEXT, score TEXT, 
    fine1 INTENGER, fine2 INTENGER, fine3 INTENGER, fine4 INTENGER)''')

    try:
        cur.execute('''INSERT INTO Competitors VALUES (?, ?, ?, ?, ?, ?, ?)''', (user_id, user_name, 0, 0, 0, 0, 0))
        connection.commit()
        connection.close()
        bot.send_message(message.chat.id, f'Очень приятно, {user_name}. Для того, чтоб получить и начать сдавать задачи напишите /contest')
    except Exception:
        bot.send_message(message.chat.id, 'Ник уже занят! Попробуйте другой!')
        bot.register_next_step_handler(message, registration)

@bot.message_handler(commands=['nick'])
def nickname(message):
    bot.send_message(message.chat.id, """Придумайте себе никнейм, который будет отображаться в рейтинге. 
    Оскорбительные будут забанены, использовать имена и фамилии можно, но необязательно.
    Для перезаписи используйте /nick.
    Если вы уже создавали ник, и необходимости создавать новый, нажмите НАЗАД.)""")
    bot.register_next_step_handler(message, name_edition)
def name_edition(message):
    user_id = message.from_user
    new_nickname = message.text
    connection = sqlite3.connect('results.sql')
    cur = connection.cursor()
    cur.execute('UPDATE Competitors SET user_name = ? WHERE user_id = ?', (new_nickname, user_id))
    bot.send_message(message.chat.id, f'Очень приятно, {new_nickname}. Для того, чтоб получить и начать сдавать задачи напишите /contest')

@bot.message_handler(commands=['contest'])
def contest(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("1")
    btn2 = types.KeyboardButton("2")
    btn3 = types.KeyboardButton("3")
    btn4 = types.KeyboardButton("4")
    btn5 = types.KeyboardButton("НАЗАД")
    markup.add(btn1,btn2,btn3,btn4, row_width=2)
    bot.send_message(message.chat.id, 'Для ответа на задачу нажмите на номер', reply_markup=markup)

@bot.message_handler(func=lambda message:True)
def handle_button(message):
    if message.text == "1":
        bot.send_message(message.chat.id, 'Ваш ответ на 1 задачу:')
        bot.register_next_step_handler(message, lambda msg, task_number = 1: check_ans(msg, task_number))
    elif message.text == "2":
        bot.send_message(message.chat.id, 'Ваш ответ на 2 задачу:')
        bot.register_next_step_handler(message, lambda msg, task_number = 2: check_ans(msg, task_number))
    elif message.text == "3":
        bot.send_message(message.chat.id, 'Ваш ответ на 3 задачу:')
        bot.register_next_step_handler(message, lambda msg, task_number = 3: check_ans(msg, task_number))
    elif message.text == "4":
        bot.send_message(message.chat.id, 'Ваш ответ на 4 задачу:')
        bot.register_next_step_handler(message, lambda msg, task_number = 4: check_ans(msg, task_number))
    elif message.text == "НАЗАД":
        bot.send_message(message.chat.id, "Доступные команды: \n/start \n/nick \n/contest")                     # непонятно, что должно происходить

def check_ans(message, task_number):
    if task_number == 1:
        if message.text == ans1:
            user_id = message.from_user
            global score1, number_of_solutions1
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('SELECT fine1 FROM Competitors WHERE user_id = ?', (user_id,))
            fine = 0.01 * cur.fetchone()[0]
            cur.execute('UPDATE Competitors SET score = ROUND(score + ?*(1-?)) WHERE user_id = ?', (score1, fine, user_id))
            connection.commit()
            connection.close()
            score1 = score1 * 0.95
            number_of_solutions1 += 1
            bot.send_message(message.chat.id, f'Верно! Вы сдали задачу {number_of_solutions1}-м. Чтобы ответить на другие задачи, нажмите на их номер')
            bot.register_next_step_handler(message, handle_button)
        else:
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('UPDATE Competitors SET fine1 = fine1 + ? WHERE user_id = ?', (5, user_id))
            connection.commit()
            connection.close()
            bot.send_message(message.chat.id, "Неверный ответ. Нажмите на номер задачи, чтобы ответить снова")
            bot.register_next_step_handler(message, handle_button)
    if task_number == 2:
        if message.text == ans2:
            user_id = message.from_user
            global score2, number_of_solutions2
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('SELECT fine2 FROM Competitors WHERE user_id = ?', (user_id,))
            fine = 0.01 * cur.fetchone()[0]
            cur.execute('UPDATE Competitors SET score = ROUND(score + ?*(1-?)) WHERE user_id = ?', (score2, fine, user_id))
            connection.commit()
            connection.close()
            score2 = score2 * 0.95
            bot.send_message(message.chat.id, f'Верно! Вы сдали задачу {number_of_solutions2}-м. Чтобы ответить на другие задачи, нажмите на их номер')
            bot.register_next_step_handler(message, handle_button)
        else:
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('UPDATE Competitors SET fine2 = fine2 + ? WHERE user_id = ?', (5, user_id))
            connection.commit()
            connection.close()
            bot.send_message(message.chat.id, "Неверный ответ. Нажмите на номер задачи, чтобы ответить снова")
            bot.register_next_step_handler(message, handle_button)
    if task_number == 3:
        if message.text == ans3:
            user_id = message.from_user
            global score3, number_of_solutions3
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('SELECT fine3 FROM Competitors WHERE user_id = ?', (user_id,))
            fine = 0.01 * cur.fetchone()[0]
            cur.execute('UPDATE Competitors SET score = ROUND(score + ?*(1-?)) WHERE user_id = ?', (score3, fine, user_id))
            connection.commit()
            connection.close()
            score3 = score3 * 0.95
            bot.send_message(message.chat.id, f'Верно! Вы сдали задачу {number_of_solutions3}-м. Чтобы ответить на другие задачи, нажмите на их номер')
            bot.register_next_step_handler(message, handle_button)
        else:
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('UPDATE Competitors SET fine3 = fine3 + ? WHERE user_id = ?', (5, user_id))
            connection.commit()
            connection.close()
            bot.send_message(message.chat.id, "Неверный ответ. Нажмите на номер задачи, чтобы ответить снова")
            bot.register_next_step_handler(message, handle_button)
    if task_number == 4:
        if message.text == ans4:
            user_id = message.from_user
            global score4, number_of_solutions4
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('SELECT fine4 FROM Competitors WHERE user_id = ?', (user_id,))
            fine = 0.01 * cur.fetchone()[0]
            cur.execute('UPDATE Competitors SET score = ROUND(score + ?*(1-?)) WHERE user_id = ?', (score4, fine, user_id))
            connection.commit()
            connection.close()
            score4 = score4 * 0.95
            bot.send_message(message.chat.id, f'Верно! Вы сдали задачу {number_of_solutions4}-м. Чтобы ответить на другие задачи, нажмите на их номер')
            bot.register_next_step_handler(message, handle_button)
        else:
            connection = sqlite3.connect('results.sql')
            cur = connection.cursor()
            cur.execute('UPDATE Competitors SET fine4 = fine4 + ? WHERE user_id = ?', (5, user_id))
            connection.commit()
            connection.close()
            bot.send_message(message.chat.id, "Неверный ответ. Нажмите на номер задачи, чтобы ответить снова")
            bot.register_next_step_handler(message, handle_button)



bot.polling(none_stop=True)