from flask import Flask, render_template, request
import pymongo
import dns

app = Flask(__name__)

@app.route('/')
def signup():
    name = request.args.get('name');
    email = request.args.get('email');
    password = request.args.get('password');

    inputs = {
        'name': name,
        'email': email,
        'password': password
    }

    def add_to_db(inputs):
        my_client = pymongo.MongoClient('mongodb+srv://vhomesgroup:vhomes2019@cluster0.rmikc.mongodb.net/VHomes?retryWrites=true&w=majority')
        my_db = my_client['VHomes']
        my_col = my_db['users']
        my_col.insert_one(inputs)

    add_to_db(inputs);

    return render_template('signup.html');

@app.route('/signup_success')
def success():
    return render_template('signup_success.html')
