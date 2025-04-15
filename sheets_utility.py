import string
import gspread
from gspread import Client, Spreadsheet, Worksheet
import random
import time
from datetime import datetime
SPREADSHEET_URL1 = 'https://docs.google.com/spreadsheets/d/19vybSydpRDYMeHPJxAD-bMm2b9HKCk88RNfVTrGjwBI/edit?gid=0#gid=0'
from vininfo import Vin

class User:
    def __init__(self):
        keys = ['vin', 'problem', 'time', 'day', 'info']
        for key in keys:
            self.key = None

    def which_vin(self, vin):
        data = ()
        obj = Vin(vin)
        data += obj.valid  # True
        data += obj.country  # Germany
        data += obj.manufacturer  # Audi
        data += obj.year  # 2013
        self.vin = data


def d(date_str, date_format="%d.%m.%Y"): #вычисляет сколько дней с начала года прошло, координата x в таблице
    date = datetime.strptime(date_str, date_format)
    start_of_year = datetime(date.year, 1, 1)
    return (date - start_of_year).days + 1

#методы sheets
# def insert(ws: Worksheet):
#     ws.insert_cols([["213213123"], ["тойота"], ["замена масла"]], col=2)
#
# def create_ws_fill_and_del(sh: Spreadsheet):
#     another_worksheet = sh.add_worksheet("another", rows=100, cols=100)
#     another_worksheet.append_rows([
#         ["E-mail", "Телефон"],
#         ["test@example.com", "+7 900 123-45-67"],
#         ["user@mail.com", "+7 901 987-65-43"]
#     ])
#     input("enter to delete ws")
#     sh.del_worksheet(another_worksheet)
#
# def find_and_print(ws: Worksheet):
#     c = ws.find("15.03.2025")
#     print( ws.cell(c.row, c.col + 1).value)

def check_time(ws, date, time):
    if ws.cell(d(date), time).value == None:
        return 1
    return 0

def check_day(ws, date):
    l = []
    date = d(date)
    row_values = ws.row_values(date)
    i = 6
    for x in row_values:
        i += 1
        if x == '_': return l
        if not x:
            l.append(i)
        print(x[:7], i)
    return l


def add_inf(ws: Worksheet, date, time, summary):
    x = d(date)
    y = int(time) - 6
    if check_time(ws, date, y):
        ws.update_cell(x, y, ' '.join(summary))
        # return f'вы предварительно записаны на {date}, {time}:00 \nнапишите свой VIN-номер'

# def add_inf(ws: Worksheet, date='15.03.2025', time=16, long=1):
#     vin = str(random.randint(100000, 1000000))
#     car_name = 'toyota'
#     chat_id = '@' + str(random.randint(100000, 1000000))
#     usluga = 'замена масла'
#     x = d(date)
#     y = time - 6
#     if check_time(ws, date, y):
#         ws.update_cell(x, y, ' '.join([vin, car_name, chat_id, usluga]))
#         print(f'клиент записан на {date}, {time}:00')
#     else:
#         print("время занято")




def main():
    start_time = time.time()
    gc: Client = gspread.service_account("../creds.json")
    sh: Spreadsheet = gc.open_by_url(SPREADSHEET_URL1)
    #worksheet = Client.open("test_sheets").worksheet("Лист1")
    ws = sh.sheet1
    print(check_day(ws, '15.03.2025'))
    # add_inf(ws,'15.03.2025', 16)
    print(time.time() - start_time)

if __name__ == '__main__':
    main()