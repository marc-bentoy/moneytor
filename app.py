import os
import psycopg2
from datetime import datetime, timezone
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(database_url)

# TODO: add the following endpoints:
    # post - /api/wallet - creates a new wallet with wallet name
    # get - /api/wallet - retreives a specified wallet with wallet id
    # post - /api/expense - inserts a new expense on the expenses table
    # post - /api/earning - inserts a new earning on the earnings table

# DATABASE QUERIES
CREATE_WALLETS_TABLE = """CREATE TABLE IF NOT EXISTS wallets (id SERIAL PRIMARY KEY, name TEXT);"""
CREATE_EXPENSES_TABLE = """CREATE TABLE IF NOT EXISTS expenses (wallet_id INTEGER, expense REAL, date TIMESTAMP, FOREIGN KEY(wallet_id) REFERENCES wallets(id) ON DELETE CASCADE);"""
CREATE_EARNINGS_TABLE = """CREATE TABLE IF NOT EXISTS earnings (wallet_id INTEGER, earning REAL, date TIMESTAMP, FOREIGN KEY(wallet_id) REFERENCES wallets(id) ON DELETE CASCADE);"""

INSERT_WALLET_RETURN_ID = "INSERT INTO wallets (name) VALUES (%s) RETURNING id;"
INSERT_EARNING = "INSERT INTO earnings (wallet_id, earning, date) VALUES (%s, %s, %s);"
INSERT_EXPENSE = "INSERT INTO expenses (wallet_id, expense, date) VALUES (%s, %s, %s);"

@app.get("/")
def home():
    return "ato ni!"


@app.post("/api/wallet")
def create_wallet():
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_WALLETS_TABLE)
            cursor.execute(INSERT_WALLET_RETURN_ID, (name,))
            wallet_id = cursor.fetchone()[0]
    
    return {"id": wallet_id, "message": f"Wallet {name} created."}, 201


@app.post("/api/earning")
def insert_earning():
    data = request.get_json()
    earning = data["earning"]
    wallet_id = data["wallet"]
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EARNINGS_TABLE)
            cursor.execute(INSERT_EARNING, (wallet_id, earning, date))
    
    return {"message": "Earning added."}, 201


@app.post("/api/expense")
def insert_expense():
    data = request.get_json()
    expense = data["expense"]
    wallet_id = data["wallet"]
    try:
        date = datetime.strptime(data["date"], "%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_EXPENSES_TABLE)
            cursor.execute(INSERT_EXPENSE, (wallet_id, expense, date))
    
    return {"message": "Expense added."}, 201