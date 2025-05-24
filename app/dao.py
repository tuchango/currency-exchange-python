from app.models import Currency, ExchangeRate


def get_all_curencies() -> list[Currency]:
    pass


def get_currency_by_code(code: str) -> Currency | None:
    pass


def add_currency(Currency) -> None:
    pass


def get_all_exchange_rates() -> list[ExchangeRate]:
    pass


def add_exchange_rate(Rate) -> None:
    pass


def get_rate(from_code, to_code) -> float:
    pass
