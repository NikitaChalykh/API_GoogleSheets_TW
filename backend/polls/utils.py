import datetime
import os

import requests
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


def get_actual_dollar_currency():
    '''Получаем курс доллара с сайта ЦБ.'''
    response = requests.get(
        'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(
            datetime.datetime.now().strftime('%d/%m/%Y')
        ))
    soup = BeautifulSoup(response.text, 'lxml-xml')
    dollar_currency_text = soup.find(ID='R01235').get_text()[-7:]
    return round(float(dollar_currency_text.replace(',', '.')), 2)


def send_telegram_message(message):
    '''Отправка уведомлений в Telegramm.'''
    token = os.getenv('TELEGRAM_TOKEN')
    bot = telegram.Bot(token)
    chat_id = os.getenv('CHAT_ID')
    bot.send_message(chat_id, message)


def check_orders_delivery_date(orders):
    '''Проверяем актуальность даты срока поставки заказа.'''
    lated_orders = []
    today_date = datetime.datetime.now().date()
    for order in orders:
        if order.delivery_date < today_date:
            lated_orders.append(order.order_number)
    return lated_orders
