import datetime

import requests
from bs4 import BeautifulSoup


def get_actual_dollar_currency():
    '''Получаем курс доллара с сайта ЦБ.'''
    response = requests.get(
        'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(
            datetime.datetime.now().strftime('%d/%m/%Y')
        ))
    soup = BeautifulSoup(response.text, 'lxml-xml')
    dollar_currency_text = soup.find(ID='R01235').get_text()[-7:]
    return round(float(dollar_currency_text.replace(',', '.')), 2)
