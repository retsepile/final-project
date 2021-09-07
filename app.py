# Retsepile Koloko
# Classroom 2
from flask import Flask, request
import sqlite3
import hmac
from flask_cors import CORS
from flask_jwt import JWT, current_identity


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


def login():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS login(user_id PRIMARY KEY,"
                    "username TEXT NOT NULL,"
                    "password TEXT NOT NULL) ")
    print("Login table created")


def client():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS clients (user_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "name_of_customer TEXT NOT NULL,"
                    "price TEXT NOT NULL,"
                    "payment TEXT NOT NULL,"
                    "date_made DATE,"
                    "time_made TIME)")
        print("Client table created")


def location():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE  IF NOT EXISTS country(id Primary Key,"
                    "name_of_continent TEXT NOT NULL,"
                    "name_of_country TEXT NOT NULL,"
                    "days_of_trip INTEGER,"
                    "images TEXT NOT NULL)")
        print("Location table created")


sign_up()
login()
client()
location()


def authenticate(username, password):
    username = username.get(username, None)
    if username and hmac.compare_digest(username.password.encode('utf-8'), password.encode('utf-8')):
        return username


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

    if request.method == "GET":
        response["data"] = "You have a working GET method"
        response["user"] = {
            "name": "Karabo",
            "email": "karabo@gmail.com"
        }
        return response

    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect('capstone.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO login("
                           "first_name,"
                           "last_name,"
                           "email,"
                           "username,"
                           "password) VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, email, username, password))
            con.commit()
            return response


@app.route('/location/', methods=["POST", "GET"])
# @jwt_required()
def insert_location():
    response = {}

    if request.method == "POST":
        name_of_continent = request.form['name_of_continent']
        name_of_country = request.form['name_of_country']
        days_of_trip = request.form['days_of_trip']
        image = request.form['image']

        with sqlite3.connect('capstone.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO country ("
                           "name_of_continent,"
                           "name_of_country,"
                           "days_of_trip,"
                           "images) VALUES(?, ?, ?,?)", (name_of_continent, name_of_country, days_of_trip, image))
            con.commit()
            response["status_code"] = 201
            response['description'] = "Inserted location successfully"
        return response

    if request.method == "GET":
        with sqlite3.connect("capstone.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM country ")
            country = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = country
        return response


@app.route('/payment/', methods=["POST", "GET"])
def payment():
    response = {}

    if request.method == "POST":
        name_of_customer = request.form['name_of_customer']
        price = request.form['price']
        payment = request.form['payment']
        date = request.form['date']
        time = request.form['time']

        with sqlite3.connect('capstone.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients("
                           "name_of_customer,"
                           "price,"
                           "payment,"
                           "date_made,"
                           "time_made) VALUES(?, ?, ?, ?, ?)", (name_of_customer, price, payment, date, time))
            conn.commit()
            response["status_code"] = 201
            response['description'] = "payment successfully"
        return response

    if request.method == "GET":
        with sqlite3.connect("capstone.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ")
            payment = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = payment
        return response


if __name__ == '__main__':
    app.run(debug=True)
