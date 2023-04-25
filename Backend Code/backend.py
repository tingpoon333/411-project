#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:50:32 2023

@author: johnkim
"""

"""
Backend Code for CS411
API 1: RAWG Video Game Database
API 2: 
"""

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask_login

#for image uploading
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'secret_for_safety'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CS460460@'
app.config['MYSQL_DATABASE_DB'] = 'gamerank'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user

@app.route("/login")
def login():
    if flask.request.method == 'GET':
        return render_template('intropage.html', login = True)
    #The request method is POST (page is recieving data)
    email = flask.request.form['email']
    cursor = conn.cursor()
	#check if email is registered
    if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
        data = cursor.fetchall()
        pwd = str(data[0][0] )
        if flask.request.form['password'] == pwd:
            user = User()
            user.id = email
            flask_login.login_user(user) #okay login in user
            return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file
    return render_template("start.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            fname=request.form.get('first_name')
            lname=request.form.get('last_name')
            email=request.form.get('email')
            password=request.form.get('password') 
        except:
            return render_template('intropage.html', signup = True)
        cursor = conn.cursor()
        test =  isEmailUnique(email)
        if test:
            print(cursor.execute("INSERT INTO Users (email, pass_word, first_name, last_name) VALUES ('{0}', '{1}', '{2}', '{3}')".format(email, password, fname, lname)))
            conn.commit()
            user = User()
            user.id = email
            flask_login.login_user(user)
            return render_template('intropage.html', signup = True)
    else:
        return render_template('intropage.html', signup = True)
        
def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True
@app.route("/back")
def back():
	return render_template('start.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('start.html')

#default page
@app.route("/", methods = ['GET'])
def hello():
	return render_template('start.html')


if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port = 7000, debug=True)
