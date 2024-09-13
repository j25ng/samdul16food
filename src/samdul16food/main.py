from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import time
import csv
import os

app = FastAPI()

origins = [
    "http://127.0.0.1:8899",
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
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    # 음식 이름과 시간을 csv로 저장 -> /code/data/food.csv
    fields = ['food', 'time']
    data = {"food": name, "time": t}

    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(data)

    return data
