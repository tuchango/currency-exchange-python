DROP TABLE IF EXISTS Currencies;
DROP TABLE IF EXISTS ExchangeRates;

CREATE TABLE Currencies (
    id          INTEGER PRIMARY KEY,
    code        TEXT,
    full_name   TEXT
);

CREATE TABLE ExchangeRates (
    id          INTEGER PRIMARY KEY,
    base_curr   INTEGER,
    target_curr INTEGER,
    rate        REAL
);
