import json
from urllib.request import urlopen
from app.dao import add_currency, add_exchange_rate, get_all_currencies, get_all_exchange_rates
from app.models import Currency, ExchangeRate
from config import ACCESS_KEY, API_URL


def list_currencies():
    return get_all_currencies()


def list_exchange_rates():
    return get_all_exchange_rates()


def fetch_currencies() -> dict | None:
    try:
        with urlopen(API_URL + '/list' + '?access_key=' + ACCESS_KEY) as req:
            data = json.load(req)
    except Exception as e:
        print(e)
        return None
    return data.get("currencies")


def fetch_exchange_rates() -> dict | None:
    try:
        with urlopen(API_URL + '/live' + '?access_key=' + ACCESS_KEY) as req:
            data = json.load(req)
    except Exception as e:
        print(e)
        return None
    return data.get("quotes")


def update_all():
    currencies = fetch_currencies()  # запрашиваем список валют

    # записываем их в бд
    for currency in currencies:
        add_currency(Currency(currency, currencies[currency]))

    exchange_rates = fetch_exchange_rates()  # запрашиваем обменные курсы к доллару

    # записываем их в бд
    for exchange_rate in exchange_rates:
        add_exchange_rate(ExchangeRate(exchange_rate[:3], exchange_rate[3:], exchange_rates[exchange_rate]))
