from flask import Flask, request, jsonify
import sqlite3
import hmac
from flask_cors import CORS
from flask_jwt import JWT, current_identity
# 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
from gunicorn.config import User


class Capstone:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def sign_up():
    with sqlite3.connect("capstone.db") as con:
        print("Database created successfully")
    con.execute("CREATE TABLE IF NOT EXISTS sign_up(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "first_name TEXT NOT NULL,"
                "last_name TEXT NOT NULL,"
                "username TEXT NOT NULL,"
                "password TEXT NOT NULL, "
                "email TEXT NOT NULL,"
                "phone INT NOT NULL)")
    print("Signup table created successfully")

def user_table():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "first_name TEXT NOT NULL,"
                 "last_name TEXT NOT NULL,"
                 "username TEXT NOT NULL,"
                 "password TEXT NOT NULL, address TEXT NOT NULL, phone_number INT NOT NULL, user_email TEXT NOT NULL)")
        print("user table created successfully")


def login():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS login(id PRIMARY KEY,"
                    "username TEXT NOT NULL,"
                    "password TEXT NOT NULL) ")
    print("Login table created")


def client():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS CLIENTS("
                    "name_of_customer TEXT NOT NULL,"
                    "total_amount TXT NOT NULL,"
                    "payment REAL)")
        print("Client table created")


def location():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE  IF NOT EXISTS country(id Primary Key AUTOINCREMENT,"
                    "name_of_continent TEXT NOT NULL,"
                    "name_of_country TEXT NOT NULL,"
                    "days_of_trip INTEGER,"
                    "date DATE,"
                    "time TIME)")
        print("Location table created")


sign_up()
user_table()
login()
client()
location()


def fetch_users():
    with sqlite3.connect('capstone.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user")

        users = cursor.fetchall()

        new_data = []

        for data in users:
            new_data.append(User(data[0], data[3], data[4]))
    return new_data

users = fetch_users()

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password, use=None):
    user = username_table.get(username, None)
    if user and hmac.compare_digest(user.password.encode('utf-8'), password.encode('utf-8')):
        return use

def identity(payload):

    id = payload['identity']
    return id.get(id, None)


app = Flask(__name__)
CORS(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)


@app.route('/protected')
def protected():
    return '%s' % current_identity


@app.route('/sign-up', methods=["POST", "GET"])
def sign_up():
    response = {}

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']

        with sqlite3.connect('capstone.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO sign_up("
                           "first_name,"
                           "last_name,"
                           "email,"
                           "phone,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, email, username, password, phone))
            con.commit()
            response["content"] = "signup successfully"
            response["status_code"] = 200
        return response


@app.route('/location/', methods=["POST"])
# @jwt_required()
def insert_location():
    response = {}

    if request.method == "POST":
        name_of_continent = request.form['name_of_continent']
        name_of_country = request.form['name_of_country']
        days_of_trip = request.form['days_of_trip']
        date = request.form['date']
        time = request.form['time']

    with sqlite3.connect('capstone.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO location ("
                       "name_of_continent,"
                       "name_of_country,"
                       "days_of_trip,"
                       "date,"
                       "time) VALUES(?, ?, ?, ?, ?)",
                       (name_of_continent, name_of_country, days_of_trip, date, time))
        conn.commit()
        response["status_code"] = 201
        response['description'] = "Inserted location successfully"
        return response


@app.route('/client', methods=["POST"])
def client():
    response = {}

    if request.method == "POST":
        name_of_customer = request.form['name_of_customer']
        total_amount = request.form['total_amount']
        payment = request.form['payment']

    with sqlite3.connect('capstone.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO client(name_of_customer,"
                       "total_amount,"
                       "payment) "
                       "VALUES(?,?,?) ", (name_of_customer, total_amount, payment))
        conn.commit()
        response["status_code"] = 201
        response['description'] = "Inserted customer  successfully"
        return response


@app.route('/get-users/', methods=['GET'])
def all_users():
    response = {}
    with sqlite3.connect("capstone.db") as conn:
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        cursor.execute("SELECT * FROM users")
        posts = cursor.fetchall()
        accumulator = []
        for i in posts:
            accumulator.append({k: i[k] for k in i.keys()})
            response['status_code'] = 200
            response['data'] = tuple(accumulator)
            return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
