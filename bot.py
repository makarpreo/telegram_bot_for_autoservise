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
user = User()
GROUP_CHAT_ID = -1001234567890
token = '6750713880:AAHRvqxi8AireZkJjwubG11KDzvHmWM5OEU'
bot = telebot.TeleBot(token)


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
    bot.register_next_step_handler(message, manage)


@bot.message_handler(content_types=['text'])
def manage(message):
    if message.text == 'записаться':
        markup = ReplyKeyboardMarkup()
        # markup.add(types.KeyboardButton('Полная замена'))
        # markup.add(types.KeyboardButton('Замена масла в двигателе'))
        # markup.add(types.KeyboardButton('Замена масла в КПП'))
        bot.send_message(
            message.chat.id,
            f"напишите удобную для вас дату в формате: \n01.01.2000",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, which_day)


def wrong_date(message):
    markup = ReplyKeyboardMarkup()
    # markup.add(types.KeyboardButton('Полная замена'))
    # markup.add(types.KeyboardButton('Замена масла в двигателе'))
    # markup.add(types.KeyboardButton('Замена масла в КПП'))
    # bot.send_message(
    #     message.chat.id,
    #     f"напишите удобную для вас дату в формате: \n01.01.2000",
    #     reply_markup=markup
    # )
    bot.register_next_step_handler(message, which_day)


def which_day(message):
    l = check_day(ws, message.text)
    markup = types.ReplyKeyboardMarkup()
    for time in l:
        markup.add(types.KeyboardButton(f"{time}:00")).row()
    text_message = message.text
    if len(l) != 0:
        bot.send_message(message.chat.id,
                         f"Выберите время", reply_markup=markup)
        bot.register_next_step_handler(message, which_time, l)
    else:
        bot.send_message(message.chat.id, f"В этот день нет свободных дат, пожалуйста, выберите другую дату")
        bot.register_next_step_handler(message, which_day)

def which_time(message, data):
    l, selected_date = data
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('отлично'))

    if ':' in message.text:
        selected_time = message.text.split(":")[0]
        msg = add_inf(ws, selected_date, selected_time)
        bot.send_message(message.chat.id, msg)
        bot.register_next_step_handler(message, start_handler)
    else:
        bot.send_message(message.chat.id, f"неверный формат сообщения")
        bot.register_next_step_handler(message, which_time, data)


def vin_info(message):
    vin_data = user.which_vin()


def send_to_group(message):
    # bot.send_message("#-4678635855", f"Сообщение от {message.chat.id}: {message.text}")
    bot.send_message(message.chat.id, f"Вы предварительно записаны на 00 00 00")
    bot.register_next_step_handler(message, start_handler)


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

# vin, нужно ли подобрать запчасти, удобные даты, чтобы механикам приходило сообщение и они подтверждали запись, потом ему приходит сообщение с инфой о автомобиле

bot.polling(none_stop=True)
