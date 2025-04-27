import sqlite3

con = sqlite3.connect('currencies.db')
cur = con.cursor()

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

cur.execute("""
    INSERT INTO Currencies (code, full_name)
    VALUES
        ('USD', 'United States Dollar'),
        ('RUB', 'Russian Ruble'),
        ('KZT', 'Tenge')
""")

cur.execute("""
    INSERT INTO ExchangeRates (base_curr, target_curr, rate)
    VALUES (
        (SELECT id FROM Currencies WHERE code = 'USD'),
        (SELECT id FROM Currencies WHERE code = 'RUB'),
        82.87
    )
""")

cur.execute("""
    INSERT INTO ExchangeRates (base_curr, target_curr, rate)
    VALUES (
        (SELECT id FROM Currencies WHERE code = 'USD'),
        (SELECT id FROM Currencies WHERE code = 'KZT'),
        514.89
    )
""")

con.commit()
