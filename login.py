from flask import request, jsonify
from flask import Flask
from flask import render_template, redirect

import json
import sqlite3
from flask_apps import app, db

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    print("enters")
    username = request.form['user_name']
    password = request.form['password']

    try:
        conn = sqlite3.connect('argupedia_database.db')
        print("CONNECTION SUCCESSFUL")
        query = "SELECT username, password FROM register_table WHERE username='" + username + '\' AND password = \'' + password +"';"
        print(query)
        cursor = conn.execute(query)
        print("Query executed successfully in register table")
        rows = cursor.fetchall()
        if(len(rows) >= 1):
            print("Account exists! Login successful")
            return render_template('')
        else:
            print("Account not found! Please register")
            return redirect('/register')
        conn.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
    return json.dumps({'status': 'success'})