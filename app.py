from flask import Flask, render_template, request, redirect, url_for
from flask_session import Session
import pymongo
import dns
import aes


URI = 'mongodb+srv://vhomesgroup:vhomes2019@cluster0.rmikc.mongodb.net/VHomes?retryWrites=true&w=majority'
KEY = 'YpzUpPSQd3NSmz1b'
cipher = aes.AESCipher(KEY)


app = Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route('/')
def index():
    return render_template('home.html');


@app.route('/home')
def home():
    return render_template('home.html');


@app.route('/contact')
def contact():
    return render_template('contact.html');


@app.route('/locations')
def locations():
    print(session.get('logged_in'))
    return render_template('locations.html', logged_in=session.get('logged_in'));


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/signup')
def signup():
    return render_template('signup.html');


@app.route('/signup_success')
def signup_success():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')

    enc_pass = cipher.encrypt(password)

    inputs = {
        'name': name,
        'email': email,
        'password': enc_pass
    }

    def check_db(email):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        user = my_col.find_one({'email': str(email)})
        return user

    def add_to_db(inputs):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        my_col.insert_one(inputs)

    if check_db(email) == None:
        add_to_db(inputs)
        response = 'sign up successful!'
        session['logged_in'] = True
        return render_template('signup_success.html', response=response)
    else:
        response = 'email already registered'
        session['logged_in'] = False
        return render_template('signup_unsuccessful.html', response=response)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login_success')
def login_success():
    email = request.args.get('email')
    password = request.args.get('password')

    inputs = {
        'email': email,
        'password': password
    }

    def get_from_db(email, password):
        my_client = pymongo.MongoClient(URI)
        my_db = my_client['VHomes']
        my_col = my_db['users']
        user = my_col.find_one({'email': str(email)})
        dec_pass = cipher.decrypt(str(user['password']))
        if str(user['email']) == email and dec_pass == password:
            return True
        else:
            return False

    if get_from_db(email, password) == False:
        response = 'incorrect username or password'
        session['logged_in'] = False
        return render_template('login_unsuccessful.html', response=response)
    else:
        response = 'logged in as ' + email
        session['logged_in'] = True
        return render_template('login_success.html', response=response)


if __name__ == '__main__':
    app.run()
