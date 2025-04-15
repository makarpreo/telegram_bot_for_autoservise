import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot import types
import asyncio
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import tracemalloc
from sheets_utility import *
# from oauth2client import *

gc: Client = gspread.service_account("../creds.json")
sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL1)
ws = sh.sheet1
SPREADSHEET_URL1 = 'https://docs.google.com/spreadsheets/d/19vybSydpRDYMeHPJxAD-bMm2b9HKCk88RNfVTrGjwBI/edit?gid=0#gid=0'


class User:
    def __init__(self):
        keys = ['car', 'problem', 'time', 'day', 'other']
        for key in keys:
            self.key = None
user = User()
# CHANNEL_USERNAME = "@priikolchikii"
# GROUP_CHAT_ID = -1001234567890
token = '6750713880:AAHRvqxi8AireZkJjwubG11KDzvHmWM5OEU'
bot = telebot.TeleBot(token)
# Состояния пользователя
user_states = {}
button_access = {}


# def check_subscription(message):
#     user_id = message.from_user.id
#
#     try:
#         chat_member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
#         if chat_member.status != 'left':
#             bot.reply_to(message, "Вы подписаны на канал!")
#         else:
#             bot.reply_to(message, "Вы не подписаны на канал. Пожалуйста, подпишитесь, чтобы продолжить.")
#
#     except Exception as e:
#         bot.reply_to(message, "Произошла ошибка при проверке подписки на канал.")


def delete_message(chat_id, message_id):
    if message_id:
        try:
            bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

# @bot.message_handler(content_types=['text'])  # Обрабатываем все сообщения
# def handle_message(message):
#     bad_words =  ["рыжий"]
#     if any(word in message.text.lower() for word in bad_words):
#         bot.send_message(message.chat.id, "Не используйте такие слова!")
#         bot.delete_message(message.chat.id, message.message_id)
#     elif message.text:
#         a = random.randint(0, 20)
#         funny_words = [
#             "Балда", "Шмяк", "Хрень", "Пердимонокль", "Пельмень", "Шарамыга", "Крендель", "Дрын", "Шалопай", "Фигляр",
#             "Бубен", "Охломон", "Вжик", "Пампушечка", "Лохматка", "Пшик", "Вундеркиндель", "Дрыщ", "Чебурахнуться",
#             "Пыхтеть",
#             "Баклажан", "Гоготун", "Лапотень", "Чикчирик", "Брык", "Дзынь", "Балабонить", "Фигли-мигли", "Карапуз",
#             "Прыщ",
#             "Шмель", "Борщ", "Куролесить", "Пупсик", "Дуралей", "Вертеп", "Дзюдоист", "Лопушок", "Переполох", "Кукуся",
#             "Дрыгоножка", "Мухосранск", "Слюнявчик", "Жмых", "Тыр-пыр", "Шараповка", "Опереточный", "Балдахин",
#             "Пирдуха", "Штопор",
#             "Вжух", "Шлёпки", "Раздолбай", "Бумс", "Чудик", "Щелбан", "Хлюпик", "Гопник", "Шелудивый", "Мямлик",
#             "Пузан", "Пельмешка", "Тюфяк", "Лопоухий", "Трепач", "Дрындулет", "Шмара", "Баламут", "Шебуршун",
#             "Мордастик",
#             "Пирожуля", "Чебурек", "Фуфло", "Шушара", "Кукундрик", "Трындец", "Жмурик", "Тарарам", "Фофан", "Дрыг",
#             "Трепетун", "Чичик", "Гамаз", "Шлап", "Шпротик", "Бухарик", "Чих-Пых", "Хохотун", "Кособокий", "Зюзя",
#             "Пень-колода", "Гуня", "Бухтелка", "Чпок", "Шикардос", "Хлебобулочный", "Штрудель", "Щекотун", "Клюква",
#             "Пыжик"
#         ]
#         if a == 2:
#             bot.send_message("@fewrfgwrefardfcwrf", random.choice(funny_words))
#             bot.register_next_step_handler(message, handle_message)

# @bot.message_handler(func=lambda message: True)
# def delete_bad_words(message):
#     bad_words = ["бля", "рыжий"]
#     if any(word in message.text.lower() for word in bad_words):
#         bot.delete_message(message.chat.id, message.message_id)
#         bot.send_message(message.chat.id, "Не используйте такие слова!")

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton("записаться"))
    markup.add(types.KeyboardButton("Другое"))
    bot.send_message(
        message.chat.id,
        f"Здравствуйте!\n\nВыберите тип услуги:",
        reply_markup=markup
    )
    # bot.register_next_step_handler(message, handle_message)




# @bot.message_handler(content_types=['text'])
# def manage(message):
#     if message.text == 'записаться':
#         markup = ReplyKeyboardMarkup()
#         # markup.add(types.KeyboardButton('Полная замена'))
#         # markup.add(types.KeyboardButton('Замена масла в двигателе'))
#         # markup.add(types.KeyboardButton('Замена масла в КПП'))
#         bot.send_message(
#             message.chat.id,
#             f"напишите удобную для вас дату в формате: \n01.01.2000",
#             reply_markup=markup
#         )
#         bot.register_next_step_handler(message, which_day)
#     #
#     if message.text == 'Другое':
#         bot.send_message("@trfyghujikol", f"ПЕНИС")
#         bot.register_next_step_handler(message, manage)
#
#
#
#
# def which_day(message):
#     l = check_day(ws, message.text)
#     text_message = message.text
#     bot.send_message(
#         message.chat.id,f"Свободны следующие часы:\n {' '.join([str(x) + ':00' for x in l])} \n Напишите, в какое время вам будет удобно")
#     bot.register_next_step_handler(message, which_time, text_message)
#
# def which_time(message, text_message):
#     print(text_message)
#     msg = add_inf(ws, text_message, message.text[:message.text.index(':')])
#     bot.send_message(message.chat.id, msg)
#     bot.register_next_step_handler(message, send_to_group)
#
#
# def send_to_group(message):
#     bot.send_message("#-4678635855", f"Сообщение от {message.chat.id}: {message.text}")
#

# def p(message):
#     chat_id = message.chat.id
#     user.car = message.text
#     print(user.car)
#     bot.register_next_step_handler(message, p)
#
#
# def second(message):
#     print(2)
#     bot.send_message(message.chat.id, '2')
#     bot.register_next_step_handler(message, start_handler)
#
#
# def third(message):
#     print(3)
#     bot.send_message(message.chat.id, '3')
#     bot.register_next_step_handler(message, start_handler)

# def maslo(message):
#     markup = ReplyKeyboardMarkup()
#     markup.add(types.KeyboardButton('Полная замена'))
#     markup.add(types.KeyboardButton('Замена масла в двигателе'))
#     markup.add(types.KeyboardButton('Замена масла в КПП'))
#     bot.send_message(
#         message.chat.id,
#         f"Выберите тип услуги:",
#         reply_markup=markup
#     )
#
# def second(message):
#     print(2)
#     bot.send_message(message.chat.id, '2')
#     bot.register_next_step_handler(message, start_handler)
#
# def third(message):
#     print(3)
#     bot.send_message(message.chat.id, '3')
#     bot.register_next_step_handler(message, start_handler)


# @bot.message_handler(content_types=['text'])
# def main(message):
#     if message.text == 'перевод СС':
#         markup = types.ReplyKeyboardMarkup()
#         btn1 = types.KeyboardButton('2->10')
#         btn2 = types.KeyboardButton('10->2')
#         markup.add(btn1, btn2)
#         msg = bot.send_message(message.chat.id, 'введитe вариант перевода', reply_markup=markup)
#         bot.register_next_step_handler(message, calc)


bot.polling(none_stop=True)
