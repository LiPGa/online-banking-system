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
from utils import add_transaction, get_balance

app = Flask(__name__)
title = "Bank Application with Flask and MongoDB"
heading = "Bank Application with Flask and MongoDB"

client = MongoClient(r"mongodb://lipgacosmosdb:RaZs2GB6Hsao2RL2lH8F5AVJdfoEBbzZeHg7vlTuX5MuuAMbQ4svG0y4QwKq5tlGodrFlrc9PeidJlgzDV8JhA==@lipgacosmosdb.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@lipgacosmosdb@") #PRIMARY CONNECTION STRING
db = client.mymongodb    #Select the database

#Select the collection name
todos = db.todo 


def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

@app.route("/")
@app.route("/list")
def lists ():
	#Display the all Tasks
	users_l = todos.find_one({"k":"users"})['v']
	users_l.sort(key=lambda x: (x["last-name"], x["first-name"], x["middle-initial"]))

	for name_dict in users_l:
		name_str = "{}/{}/{}".format(name_dict['first-name'], name_dict['middle-initial'], name_dict['last-name'])
		account_id = todos.find_one({"k": name_str})['v']
		cur_balance = get_balance(account_id, time.time())
		name_dict["account_id"] = account_id
		name_dict["cur_balance"] = cur_balance

	a1="active"
	return render_template('index.html',a1=a1,users=users_l,t=title,h=heading)


@app.route("/new_account", methods=['POST','GET'])
def new_account():
	#Adding an account
	first_name  = request.values.get("firstname")
	last_name  = request.values.get("lastname")
	middle_initial  = request.values.get("middlename")
	tax_id = request.values.get("taxid")
	contact_info = request.values.get("contactinfo")
	date = request.values.get("date")
	account_id = ''.join(random.choice(string.digits) for _ in range(10))
	
	name_str = "{}/{}/{}".format(first_name, middle_initial, last_name)
	
	name_dict = {}
	name_dict["first-name"] = first_name
	name_dict["last-name"] = last_name
	name_dict["middle-initial"] = middle_initial
	
	meta_data = {
		"first-name":first_name, "last-name":last_name, "middle-initial":middle_initial,
		"tax-id":tax_id, "contact-info":contact_info, "created-date": date
	}

	todos.update({"k": "users"}, {'$addToSet':{ "v": name_dict}}, upsert=True)
	todos.insert({"k": name_str, "v": account_id})
	todos.insert({"k": account_id, "v": meta_data})

	return redirect("/list")

@app.route("/deposit", methods=['GET', 'POST'])
def deposit():
	#Updating a Task with various references
	amount = float(request.values.get("amount"))
	account_id = request.values.get("account_id")
	timestamp = time.time()
	current_date = datetime.fromtimestamp(timestamp)
	current_month = str(current_date)[:7]
	if amount <= 0:
		print("ERROR: Amount must be greater than 0!")
		return redirect("/")
	cur_balance = get_balance(account_id, timestamp)

	# mutate the current balance
	cur_balance += amount
	add_transaction(account_id, "Deposit", timestamp, current_month, amount, cur_balance)
	return redirect("/")


@app.route("/withdraw", methods=['GET', 'POST'])
def withdraw():
	#Updating a Task with various references
	amount = float(request.values.get("amount"))
	account_id = request.values.get("account_id")
	timestamp = time.time()
	current_date = datetime.fromtimestamp(timestamp)
	current_month = str(current_date)[:7]

	if amount <= 0:
		print("ERROR: Amount must be greater than 0!")
		return redirect("/")

	cur_balance = get_balance(account_id, timestamp)

	# mutate the current balance
	if cur_balance < amount :
		print(f"ERROR: Not enough money for withdraw, current balance: {cur_balance}, withdraw amount: {amount}")
		return redirect("/")

	cur_balance -= amount
	add_transaction(account_id, "Withdraw", timestamp, current_month, amount, cur_balance)
	return redirect("/")

@app.route("/transfer", methods=['GET', 'POST'])
def transfer():
	#Updating a Task with various references
	amount = float(request.values.get("amount"))
	src_id = request.values.get("src_id")
	target_id = request.values.get("target_id")
	timestamp = time.time()
	current_date = datetime.fromtimestamp(timestamp)
	current_month = str(current_date)[:7]

	if amount <= 0:
		print("ERROR: Amount must be greater than 0!")
		return redirect("/")
	src_balance = get_balance(src_id, timestamp)
	target_balance = get_balance(target_id, timestamp)
	if src_balance < amount :
		print(f"ERROR: Not enough money for withdraw, current balance: {src_balance}, withdraw amount: {amount}")
		return redirect("/")
	src_balance -= amount
	target_balance += amount
	add_transaction(src_id, "Withdraw", timestamp, current_month, amount, src_balance)
	add_transaction(target_id, "Deposit", timestamp, current_month, amount, target_balance)
	return redirect("/")

@app.route("/dashboard", methods=['GET'])
def dashboard():
	account_id = request.values.get("account_id")
	if todos.find({'k': account_id}).count() == 0: 
		print("ERROR: Account {} does not exist".format(account_id))
		return redirect("/")

	timestamp = time.time()
	meta_data = todos.find_one({'k': account_id})['v']
	cur_balance = get_balance(account_id, timestamp)
	meta_data["cur_balance"] = cur_balance

	# Fetch transaction history in this month 
	dt_object = datetime.fromtimestamp(timestamp)
	year_month = str(dt_object)[:7]
	transaction_key = os.path.join(str(account_id), year_month)
	if todos.find({'k': transaction_key}).count() == 0: 
		trans_l = []
	else: trans_l = todos.find_one({'k': transaction_key})['v']
	return render_template('dashboard.html',data=meta_data, trans=trans_l,h=heading,t=title)

@app.route("/audit", methods=['GET'])
def audit():
	a2="active"

	if todos.find({'k': "users"}).count() == 0: 
		users_l = []
	else: users_l = todos.find_one({"k":"users"})['v']
	users_l.sort(key=lambda x: (x["last-name"], x["first-name"], x["middle-initial"]))

	# Parse the current month
	dt_object = datetime.fromtimestamp(time.time())
	year_month = str(dt_object)[:7]
	
	trans_l = []
	
	for name_dict in users_l:
		name_str = "{}/{}/{}".format(name_dict['first-name'], name_dict['middle-initial'], name_dict['last-name'])
		account_id = todos.find_one({"k": name_str})['v']
		transaction_key = os.path.join(str(account_id), year_month)
		if todos.find({'k': transaction_key}).count() == 0: 
			trans_l.append([])
		else: 
			trans_l.append(todos.find_one({'k': transaction_key})['v'])
	return render_template('audit.html',a2=a2, len=len(users_l), users=users_l, trans=trans_l,h=heading,t=title)

if __name__ == "__main__":

    app.run()
