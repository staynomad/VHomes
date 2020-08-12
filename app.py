from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pymongo
import dns

load_dotenv()
URI = os.getenv('URI')
app = Flask(__name__)

@app.route('/')
def signup():
    return render_template('signup.html');

@app.route('/signup_success')
def success():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')

    inputs = {
        'name': name,
        'email': email,
        'password': password
    }

    def add_to_db(inputs):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        my_col.insert_one(inputs)

    add_to_db(inputs);
    return render_template('signup_success.html')

@app.route('/login')
def login():
    return render_template('login.html')
