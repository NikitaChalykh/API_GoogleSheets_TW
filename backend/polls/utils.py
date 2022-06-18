import datetime
import os

import apiclient.discovery
import httplib2
import requests
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from orders.models import GoodsOrder

load_dotenv()

FORMAT = '%d.%m.%Y'


def get_actual_dollar_currency():
    '''Получаем курс доллара с сайта ЦБ.'''
    response = requests.get(
        'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(
            datetime.datetime.now().strftime('%d/%m/%Y')
        ))
    soup = BeautifulSoup(response.text, 'lxml-xml')
    dollar_currency_text = soup.find(ID='R01235').get_text()[-7:]
    return round(float(dollar_currency_text.replace(',', '.')), 2)


def check_orders_delivery_date(orders):
    '''Проверяем актуальность даты срока поставки заказа.'''
    lated_orders = []
    today_date = datetime.datetime.now().date()
    for order in orders:
        if order.delivery_date < today_date:
            lated_orders.append(order.order_number)
    return lated_orders


def get_data_in_sheets():
    '''Получаем данные из гугл талицы с заказами.'''
    CREDENTIALS_FILE = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'credentials.json'
    )
    ranges = ["Лист1!A2:D"]
    spreadsheetId = '1OpCylqw4U-64lMKZFVk7fhllqOvczTD5eb516aDghbo'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)
    results = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId,
        ranges=ranges,
        valueRenderOption='FORMATTED_VALUE',
        dateTimeRenderOption='FORMATTED_STRING'
    ).execute()
    sheet_values = tuple(results['valueRanges'][0]['values'])
    return sheet_values


def send_telegram_message(message):
    '''Отправка уведомлений в Telegramm.'''
    bot = telegram.Bot('2045985373:AAF9T9ZtOwCdA0kOzsDmdfgX6CKaskZylks')
    chat_id = os.getenv('CHAT_ID')
    bot.send_message(
        chat_id,
        'Срок поставки заказа(ов) №{} истек'.format(
            ', '.join([str(x) for x in message])
        )
    )


def create_orders(sheets_orders):
    '''Функция для группового создания объектов
    в БД по данным из google sheets.
    '''
    new_orders = []
    for sheets_order in sheets_orders:
        dollar_currency = get_actual_dollar_currency()
        new_orders.append(GoodsOrder(
            serial_number=int(sheets_order[0]),
            order_number=int(sheets_order[1]),
            dollar_value=int(sheets_order[2]),
            rub_value=dollar_currency * int(sheets_order[2]),
            delivery_date=datetime.datetime.strptime(sheets_order[3], FORMAT)
        ))
    GoodsOrder.objects.bulk_create(new_orders)
