import json
import sqlite3
from urllib.request import urlopen


API_URL = "http://localhost:8000"
ACCESS_KEY = 'dff5d216fd9de66bfd816b3703cad9c7'

con = sqlite3.connect('currencies.db')
cur = con.cursor()


def update_db_from_api():

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
        con.execute("INSERT INTO Currencies (code, full_name) VALUES (?, ?)", (currency, currencies[currency]))
    
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
        con.execute(
            """
                INSERT INTO ExchangeRates (base_curr, target_curr, rate)
                VALUES (
                    (SELECT id FROM Currencies WHERE code = ?),
                    (SELECT id FROM Currencies WHERE code = ?),
                    ?
                )
            """, (exchange_rate[:3], exchange_rate[3:], exchange_rates[exchange_rate]))
        
    con.commit()

def create_db_and_fill_it():
    cur.execute("DROP TABLE IF EXISTS Currencies")
    cur.execute("DROP TABLE IF EXISTS ExchangeRates")

    cur.execute("""
        CREATE TABLE Currencies (
            id          INTEGER PRIMARY KEY,
            code        TEXT,
            full_name   TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE ExchangeRates (
            id          INTEGER PRIMARY KEY,
            base_curr   INTEGER,
            target_curr INTEGER,
            rate        REAL
        )
    """)

    con.commit()

    update_db_from_api()


if __name__ == "__main__":
    create_db_and_fill_it()
