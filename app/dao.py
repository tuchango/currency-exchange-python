import sqlite3
from app.models import Currency, ExchangeRate

DB_PATH = "currencies.db"


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_all_curencies() -> list[Currency]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT code, full_name FROM Currencies")
    rows = cur.fetchall()
    conn.close()
    return [Currency(row["code"], row["full_name"]) for row in rows]


def get_currency_by_code(code: str) -> Currency | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT code, full_name FROM Currencies WHERE code = ?", (code,))
    row = cur.fetchone()
    conn.close()
    
    if row:
        return Currency(row["code"], row["full_name"])
    return None


def add_currency(currency: Currency) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO Currencies (code, full_name) VALUES (?, ?)",
    # -- ON CONFLICT(code) DO UPDATE SET full_name=excluded.full_name
        (currency.code, currency.full_name)
    )
    conn.commit()
    conn.close()


def get_all_exchange_rates() -> list[ExchangeRate]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT base_curr, target_curr, rate FROM ExchangeRates")
    rows = cur.fetchall()
    conn.close()
    return [ExchangeRate(row["base_curr"], row["target_curr"], row["rate"]) for row in rows]


def add_exchange_rate(exchange_rate: ExchangeRate) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ExchangeRates (base_curr, target_curr, rate)
                VALUES (
                    (SELECT id FROM Currencies WHERE code = ?),
                    (SELECT id FROM Currencies WHERE code = ?),
                    ?
                )
        """,
        (exchange_rate.base_curr, exchange_rate.target_curr, exchange_rate.rate)
    )
    conn.commit()
    conn.close()


def get_exchange_rate(from_code, to_code) -> float | None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT rate FROM ExchangeRates WHERE base_curr = ? AND target_curr = ?",
                (from_code, to_code)
    )
    row = cur.fetchone()
    conn.close()
    
    if row:
        return row["rate"]
    return None
