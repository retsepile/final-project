# Retsepile Koloko
# Classroom 2
#  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
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
                    "email TEXT NOT NULL)")
    print("Signup table created successfully")


def login():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS login(user_id PRIMARY KEY,"
                    "username TEXT NOT NULL,"
                    "password TEXT NOT NULL) ")
    print("Login table created")
    con.commit()


def client():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE IF NOT EXISTS clients (booking_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "user_id TEXT NOT NULL,"
                    "from_date INTEGER,"
                    "to_date INTEGER,"
                    "payment TEXT NOT NULL)")
        print("Client table created")


def location():
    with sqlite3.connect("capstone.db") as con:
        con.execute("CREATE TABLE  IF NOT EXISTS country(id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "name_of_continent TEXT NOT NULL,"
                    "name_of_country TEXT NOT NULL,"
                    "price TEXT NOT NULL,"
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


@app.route('/sign-up', methods=["POST", "GET", "PATCH"])
def sign_up():
    response = {}
    # registration
    if request.method == "POST":
        try:
            first_name = request.json['first_name']
            last_name = request.json['last_name']
            email = request.json['email']
            username = request.json['username']
            password = request.json['password']

            with sqlite3.connect('capstone.db') as con:
                cursor = con.cursor()
                cursor.execute("INSERT INTO sign_up ("
                               "first_name,"
                               "last_name,"
                               "email,"
                               "username,"
                               "password) VALUES(?, ?, ?, ?, ?)",
                               (first_name, last_name, email, username, password))
                con.commit()
                response['message'] = "sign up successful"
        except ValueError:
            response["message"] = "Error in registration"
        return response

    if request.method == "GET":
        with sqlite3.connect("capstone.db") as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM sign_up")
            sign_up = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = sign_up
        return response

    # login route
    if request.method == "PATCH":
        username = request.json["username"]
        password = request.json["password"]

        with sqlite3.connect("capstone.db") as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM sign_up WHERE username=? AND password=?", (username, password))
            login = cursor.fetchone()
            response['status_code'] = 200
            response['data'] = login
        return response

# route for fetching the places


@app.route('/location/', methods=["POST", "GET"])
def insert_location():
    response = {}

    if request.method == "POST":
        name_of_continent = request.form['name_of_continent']
        name_of_country = request.form['name_of_country']
        price = request.form['price']
        image = request.form['image']

        with sqlite3.connect('capstone.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO country ("
                           "name_of_continent,"
                           "name_of_country,"
                           "price,"
                           "images) VALUES(?, ?, ?,?)", (name_of_continent, name_of_country, price, image))
            con.commit()
            response["status_code"] = 201
            response['description'] = "Inserted location successfully"
        return response

    if request.method == "GET":
        with sqlite3.connect("capstone.db") as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM country ")
            country = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = country
        return response

# payment process


@app.route('/payment/', methods=["POST", "GET"])
def payment_of_place():
    response = {}

    if request.method == "POST":
        user_id = request.json['user_id']
        from_date = request.json['from_date']
        to_date = request.json['to_date']
        payment = request.json['payment']

        with sqlite3.connect('capstone.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clients("
                           "user_id,"
                           "from_date,"
                           "to_date,"
                           "payment ) VALUES(?, ?, ?, ?)", (user_id, from_date, to_date, payment))
            conn.commit()
            response["status_code"] = 201
            response['description'] = "payment successful"
        return response

    if request.method == "GET":
        with sqlite3.connect("capstone.db") as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM clients ")
            payment = cursor.fetchall()

        response['status_code'] = 200
        response['data'] = payment
        return response


# @app.route("/booking/<int:user_id>", methods=["POST"])
# def booking(user_id):
#  response = {}
# user_id = user_id
    # name_of_customer = request.form['name_of_customer']
    # days_of_trip = request.form['days_of_trip']
    # payment = request.form['payment']
    # date = request.form['date']
    # time = request.form['time']

    # if request.method == "POST":
#  with sqlite3.connect("capstone.db") as con:
#     cursor = con.cursor()
#    cursor.execute("INSERT INTO client ("
#                  "user_id"
#                 "name_of_customer,"
#                "days_of_trip,"
#               "payment,"
#              "date,"
#       "time) VALUES(?, ?, ?, ?, ?)", (user_id, name_of_customer, days_of_trip, payment, date, time))
# con.commit()
# response["message"] = "boooking made successful"
# response["status_code"] = 200
# response['data'] = {
#   "user_id": user_id,
#  "name_of_customer": name_of_customer,
# "days_of_trip": days_of_trip,
# "payment ": payment,
# 'date': date,
# "time": time
# }


if __name__ == '__main__':
    app.run(debug=True)
