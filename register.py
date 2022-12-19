from flask import request, jsonify
from flask import Flask
from flask import render_template, redirect, flash
import sqlalchemy
from sqlalchemy import engine, create_engine
import json
import sqlite3

from sqlalchemy.orm import declarative_base

from sqlalchemy_models import register_table
from flask_apps import app, db

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///database.db')
#engine = create_engine('sqlite:///database.db')
#db = declarative_base()
#db.metadata.reflect(engine)
#app.config['SECRET_KEY'] = "random"
#db = sqlalchemy(app)

@app.route('/register_page11')
def register_page():
    return render_template('register.html')

@app.route('/register11',methods=['POST'])
def register():
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    username = request.form['user_name']
    email = request.form['email']
    #gender = request.form['gender']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    print("success")
    if(password !=  confirm_password):
        print("confirm password not the same as password. Enter data again")
        return render_template('register.html')

    try:
        data = register_table(firstname, lastname, username, email, password, confirm_password)
        db.session.add(data)
        db.ssession.commit()
        flash('Record added successfully ')
    except:
        print("Error adding data")
    return render_template('login.html')

#    try:
#        conn = sqlite3.connect('argupedia_database.db')
#        query = "INSERT INTO register_table(firstname, lastname, username, email, password, confirmpassword) VALUES ('" + firstname + '\',\'' + lastname + '\',\'' + username + '\',\'' + email + '\',\'' + password + '\',\'' + confirm_password +"')"
#        print(query)
#        cursor = conn.execute( query )
#        conn.commit()
#        print("Record inserted successfully into register table")
#        conn.close()

#    except sqlite3.Error as error:
#        print("Error while connecting to sqlite", error)
#    finally:
#        if conn:
#            conn.close()
#            print("The SQLite connection is closed")
#    return json.dumps({'status': 'success'})

    ## https://codehandbook.org/python-flask-jquery-ajax-post/

if __name__ == '__main__':
    app.run(debug=True)