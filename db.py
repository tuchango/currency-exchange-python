import json
import sqlite3
from urllib.request import urlopen
from app.dao import add_currency, add_exchange_rate
from app.models import Currency, ExchangeRate


API_URL = "http://localhost:8000"
ACCESS_KEY = 'dff5d216fd9de66bfd816b3703cad9c7'


def update_db_from_api():
    con = sqlite3.connect('currencies.db')

    # запрашиваем список валют
    try:
        with urlopen(API_URL + '/list') as req:
            data = json.load(req)
    except Exception as e:
        print(e)
        return None

    currencies = data.get("currencies")

    # записываем их в бд
    for currency in currencies:
        add_currency(Currency(currency, currencies[currency]))

    con.commit()

    # запрашиваем обменные курсы к доллару
    try:
        with urlopen(API_URL + '/live') as req:
            data = json.load(req)
    except Exception as e:
        print(e)
        return None

    exchange_rates = data.get("quotes")

    # записываем их в бд
    for exchange_rate in exchange_rates:
        add_exchange_rate(ExchangeRate(exchange_rate[:3], exchange_rate[3:], exchange_rates[exchange_rate]))
        
    con.commit()
    con.close()

def create_db_and_fill_it():
    with open('db/schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect('currencies.db')
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

    update_db_from_api()


if __name__ == "__main__":
    create_db_and_fill_it()
