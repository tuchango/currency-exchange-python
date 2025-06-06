from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from app.services import list_currencies, list_exchange_rates
from config import ACCESS_KEY


# API_URL = "https://api.exchangerate.host"


# def fetch_rate(ACCESS_KEY: str, from_curr: str, to_curr: str, amount: float) -> float | None:
#     """
#     Запрашивает курс base → target у exchangerate.host.
#     Вернёт float или None, если что-то пошло не так.
#     """
#     query = f"/convert?access_key={ACCESS_KEY}&from={from_curr}&to={to_curr}&amount={amount}"
#     try:
#         with urlopen(API_URL + query) as req:
#             data = json.load(req)
#     except Exception:
#         return None

#     # проверяем успех и наличие нужного поля
#     result = data.get("result")
#     return result


class SimpleHTMLHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if self.path == "/currencies":
            data = list_currencies()  # возвращает list[Currency]
            body = json.dumps([c.__dict__ for c in data]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/exchangeRates":
            data = list_exchange_rates()  # возвращает list[ExchangeRates]
            body = json.dumps([c.__dict__ for c in data]).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)
        
        elif path == "/convert":
            query = parse_qs(parsed.query)  # вернёт dict ключ-значение
            from_curr = query.get('from', [None])[0]
            to_curr = query.get('to', [None])[0]
            amount_str = query.get('amount', [None])[0]

            if None in (from_curr, to_curr, amount_str):
                self.send_error(400, 'Incomplete data set')
                return
            
            try:
                amount = float(amount_str)
            except ValueError:
                return self.send_response(400, "amount должно быть числом")

            result = fetch_rate(ACCESS_KEY, from_curr, to_curr, amount)
            if result is None:
                return self.send_response(404, f"Курс {from_curr} / {to_curr} не найден")

            response = {
                "from":     from_curr,
                "to":       to_curr,
                "amount":   amount,
                "result":   result,
            }
            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path == '/live':
            response = {
                "success": True,
                "terms": "https://exchangerate.host/terms",
                "privacy": "https://exchangerate.host/privacy",
                "timestamp": 1430401802,
                "source": "USD",
                "quotes": {
                    "USDAED": 3.672982,
                    "USDAFN": 57.8936,
                    "USDALL": 126.1652,
                    "USDAMD": 475.306,
                    "USDANG": 1.78952,
                    # === #
                    "USDRUB": 82.87,
                    "USDKZT": 514.89
                }
            }
            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif path == '/list':
            response = {
                "success": True,
                "terms": "https://exchangerate.host/terms",
                "privacy": "https://exchangerate.host/privacy",
                "currencies": {
                    "AED": "United Arab Emirates Dirham",
                    "AFN": "Afghan Afghani",
                    "ALL": "Albanian Lek",
                    "AMD": "Armenian Dram",
                    "ANG": "Netherlands Antillean Guilder",
                    # === #
                    "USD": "United States Dollar",
                    "RUB": "Russian Ruble",
                    "KZT": "Tenge"
                }
            }
            body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            html = "<h1>Hello, Converter!</h1>".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)
