import sqlite3

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"

INSERT_CARD = "INSERT INTO card (number, pin) VALUES(?, ?);"

GET_ALL_CARDS = "SELECT * FROM card"


# Initalize Connection to DB
connection = sqlite3.connect('card.s3db')

# create Cursor object
cursor = connection.cursor()
cursor.execute(CREATE_TABLE)