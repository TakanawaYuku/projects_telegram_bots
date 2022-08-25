#Импортируем telebot
from telebot import telebot as tb
#Импортируем токен бота из config.py
from config import Token_Telegram_Bot

HELP = """
/help - Вывести список доступных команд
/add - добавить задачу в список(название задачи запрашиваем у пользователя)
/show - напечать все добавленные задачи
/exit - выход из программы
/random - добавлять случайную задачу на дату Сегодня
"""

tasks = {}


def add_todo(date, task):
    if date in tasks:
        #Дата есть в словаре
        #Добавляем задачу в список задача
        tasks[date].append(task)

    else:
        #Даты в словаре нет
        #Создаем запись в списке задач
        tasks[date] = []
        tasks[date].append(task)


#Создаем переменную типа этот тип содержится в библиотеке telebot и ей нужен обязательно токен бота.
# Создав такую переменную мы можем использовать функции
bot = tb.TeleBot(Token_Telegram_Bot)


#Создаем команду Help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, HELP)


#Создаем команду для добавления задачи
@bot.message_handler(commands=['add'])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    add_todo(date, task)
    text = f'Задача {task} добавлена на дату {date}'

    bot.send_message(message.chat.id, text)


#Создаем команду для просмотра задачи
@bot.message_handler(commands=['show'])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ''

    if date in tasks:
        text = date.upper() + '\n'
        for task in tasks[date]:
            text = text + '-' + task + '\n'

    else:
        text = 'Задач на эту дату нет'

    bot.send_message(message.chat.id, text)


#Создали декоратор, и зарегестрировали функцию для все типов сообщенией с типом 'text'
@bot.message_handler(content_types=['text'])
#Функция обработчик
def echo(message):
    bot.send_message(message.chat.id, message.text)


#Постоянно обращается к серверам телеграмма
bot.polling(none_stop=True)
