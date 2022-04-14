from uuid import NAMESPACE_URL
from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId
from more_itertools import first, last # For ObjectId to work
from pymongo import MongoClient
import os
from datetime import datetime
from dateutil.rrule import rrule, MONTHLY
import string
import json
import random
import time

client = MongoClient(r"mongodb://lipgacosmosdb:RaZs2GB6Hsao2RL2lH8F5AVJdfoEBbzZeHg7vlTuX5MuuAMbQ4svG0y4QwKq5tlGodrFlrc9PeidJlgzDV8JhA==@lipgacosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@lipgacosmosdb@") #PRIMARY CONNECTION STRING
db = client.mymongodb   #Select the database

#Select the collection name
todos = db.todo 

def get_balance(account_id, timestamp):
    # Generate the month list using current month and created month
    created_date = todos.find_one({"k":account_id})['v']["created-date"]
    created_date = datetime.strptime(created_date, "%Y-%m-%d").date()
    current_date = datetime.fromtimestamp(timestamp)
    current_month = str(current_date)[:7]

    dates = [dt for dt in rrule(MONTHLY, dtstart=created_date, until=current_date)]
    month_list = [str(dt)[:7] for dt in dates]+[current_month]
    month_list = month_list[::-1]

    # Fetch the latest transaction using the month list
    latest_month = -1
    for year_month in month_list:
        transaction_list_key = os.path.join(str(account_id), year_month)
        if todos.find({'k': transaction_list_key}).count() == 0: 
            continue
        else:	
            latest_month = year_month
            break

    # Get the current balance from the latest transaction
    if latest_month==-1: cur_balance = 0;
    else:
        latest_transaction = todos.find_one({"k":transaction_list_key})['v'][-1]
        cur_balance = latest_transaction["cur_balance"]

    return cur_balance


def add_transaction(account_id, trans_type, timestamp, current_month, amount, new_balance):
    # construct the new transaction and put into the account's transaction list
    transaction_list_key = os.path.join(str(account_id), current_month)
    transaction_dict = {
        "type": trans_type,
        "cur_balance": new_balance,
        "image" : "Image goes here!",
        "created_time" : str(datetime.fromtimestamp(timestamp)),
        "amount" : amount
    }
    todos.update({"k": transaction_list_key}, {'$addToSet':{ "v": transaction_dict}}, upsert=True)
