from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import random

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot import types
import asyncio
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from sheets_utility import *
from sheets_utility import add_inf

gc: Client = gspread.service_account("../creds.json")
sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL1)
ws = sh.sheet1
SPREADSHEET_URL1 = 'https://docs.google.com/spreadsheets/d/19vybSydpRDYMeHPJxAD-bMm2b9HKCk88RNfVTrGjwBI/edit?gid=0#gid=0'
user = User()
GROUP_CHAT_ID = -1001234567890
token = '6750713880:AAHRvqxi8AireZkJjwubG11KDzvHmWM5OEU'
bot = telebot.TeleBot(token)

# 📂 Словарь для хранения данных пользователей
user_data = {}


# 👤 Состояния
class BookingState:
    CHOOSING_DATE = "choosing_date"
    CHOOSING_TIME = "choosing_time"
    ENTERING_VIN = "entering_vin"
    CHOOSING_PARTS = "choosing_parts"
    DESCRIBING_ISSUE = "describing_issue"


# 🔘 Старт
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("записаться"))
    bot.send_message(message.chat.id, "Здравствуйте! Нажмите кнопку, чтобы записаться", reply_markup=markup)


# 🔘 Кнопка "записаться"
@bot.message_handler(func=lambda msg: msg.text.lower() == "записаться")
def start_booking(message):
    user_data[message.chat.id] = {'state': BookingState.CHOOSING_DATE}
    bot.send_message(message.chat.id, "Введите дату в формате 01.01.2025")


# 📅 Дата
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id][
    'state'] == BookingState.CHOOSING_DATE)
def handle_date(message):
    user_data[message.chat.id]['date'] = message.text
    user_data[message.chat.id]['state'] = BookingState.CHOOSING_TIME
    bot.send_message(message.chat.id, f"Вы выбрали дату: {message.text}")
    bot.send_message(message.chat.id, "Теперь выберите время (например, 14:00)")


# 🕒 Время
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id][
    'state'] == BookingState.CHOOSING_TIME)
def handle_time(message):
    user_data[message.chat.id]['time'] = message.text
    user_data[message.chat.id]['state'] = BookingState.ENTERING_VIN
    bot.send_message(message.chat.id, "Введите VIN номер автомобиля")


# 🧾 VIN
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id][
    'state'] == BookingState.ENTERING_VIN)
def handle_vin(message):
    user_data[message.chat.id]['vin'] = message.text
    user_data[message.chat.id]['state'] = BookingState.CHOOSING_PARTS

    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Да"), KeyboardButton("Нет"))
    bot.send_message(message.chat.id, "Нужно ли подобрать запчасти?", reply_markup=markup)


# 🔧 Подбор запчастей
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id][
    'state'] == BookingState.CHOOSING_PARTS)
def handle_parts(message):
    user_data[message.chat.id]['need_parts'] = message.text.lower() == "да"
    user_data[message.chat.id]['state'] = BookingState.DESCRIBING_ISSUE
    bot.send_message(message.chat.id, "Опишите проблему (например: стучит мотор, не крутит стартер)")


# 🛠️ Описание проблемы
@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id][
    'state'] == BookingState.DESCRIBING_ISSUE)
def handle_issue(message):
    user_data[message.chat.id]['issue'] = message.text

    summary = (
        f"📅 Дата: {user_data[message.chat.id]['date']}\n"
        f"🕒 Время: {user_data[message.chat.id]['time']}\n"
        f"🔢 VIN: {user_data[message.chat.id]['vin']}\n"
        f"⚙️ Подобрать запчасти: {'Да' if user_data[message.chat.id]['need_parts'] else 'Нет'}\n"
        f"🛠️ Проблема: {user_data[message.chat.id]['issue']}"
    )
    c = f"Подобрать запчасти: {'Да' if user_data[message.chat.id]['need_parts'] else 'Нет'}"
    add_inf(ws, user_data[message.chat.id]['date'], user_data[message.chat.id]['time'].split(":")[0], [user_data[message.chat.id]['issue'], c, user_data[message.chat.id]['vin']])
    bot.send_message(message.chat.id, f"✅ Вы записаны!\n\n{summary}")
    #bot.send_message(message.chat.id, f"{summary}") доделать отправку в чат
    # Очистить данные пользователя после завершения
    del user_data[message.chat.id]

bot.polling(none_stop=True)