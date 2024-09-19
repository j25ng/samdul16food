from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pickle
import pymysql
import pytz
import csv
import os

app = FastAPI()

origins = [
    "http://127.0.0.1:8899",
    "http://localhost:8899",
    "https://samdul-16-food.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#home_path = os.path.expanduser('~')
#file_path = f"{home_path}/code/data/food.csv"
file_path = "/code/data/food.csv"

if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

@app.get("/")
def read_root():
    return {"Hello": "n16"}

@app.get("/food")
def food(name: str):
    # 시간을 구함
    k_time = datetime.now(pytz.timezone('Asia/Seoul'))
    t = k_time.strftime('%Y-%m-%d %H:%M:%S')

    data = {"food": name, "time": t}
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    with open(file_path, 'a', newline='') as f:
        csv.DictWriter(f, fieldnames=['food', 'time']).writerow(data)

    db = pymysql.connect(
            host = os.getenv("DB_IP", "localhost"),
            port = int(os.getenv("DB_PORT", "33306")),
            user = 'food',
            passwd = '1234',
            db = 'fooddb',
            cursorclass=pymysql.cursors.DictCursor
            #charset = 'utf8'
    )
    #cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = "INSERT INTO foodhistory(username, foodname, dt) VALUES(%s, %s, %s)"
    with db:
        with db.cursor() as cursor:
            cursor.execute(sql, ('n16', name, t))
        db.commit()

    return data
