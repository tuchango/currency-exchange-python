class Currency():
    def __init__(self, code: str, full_name: str) -> None:
        self.code = code
        self.full_name = full_name


class ExchangeRate():
    def __init__(self, base_curr: str, target_curr: str, rate: str) -> None:
        self.base_curr = base_curr
        self.target_curr = target_curr
        self.rate = rate
