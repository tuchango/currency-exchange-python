import sqlite3
from app.services import update_all


def create_db_and_fill_it():
    with open('db/schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect('currencies.db')
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

    update_all()


if __name__ == "__main__":
    create_db_and_fill_it()
