# Store this code in 'app.py' file

import re
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo_get_database import get_database
import logging
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
dbname = get_database()

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)


app.secret_key = 'your secret key'


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		users = dbname["Users"]
		account = users.find_one({"username": username, "password": password})
		if account:
			session['loggedin'] = True
			session['id'] = str(account['_id'])
			session['username'] = account['username']
			session['email'] = account['email']
			msg = 'Logged in successfully !'
			stocks = dbname["Stocks"].find({ "email": session['email']})
			return render_template('index.html', msg=msg, stocks=stocks)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	session.pop('email', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		users = dbname["Users"]
		account = users.find_one({"username" : username})
		app.logger.info('account:%s', account)
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			users.insert_one({"username":username, "password": password, "email": email})
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)
