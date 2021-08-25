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
    con = sqlite3.connect("capstone.db")
    print("Database created successfully")
    con.execute("CREATE TABLE sign-up("
                "first_name TEXT NOT NULL,"
                "last_name TEXT NOT NULL,"
                "email TEXT NOT NULL,"
                "username TEXT NOT NULL,"
                "password TEXT NOT NULL) ")
    print("Sign-in table created")
    con.close()


def login():
    con = sqlite3.connect("capstone.db")
    con.execute("CREATE TABLE login(id PRIMARY KEY,"
                "username TEXT NOT NULL,"
                "password TEXT NOT NULL) ")
    print("Login table created")
    con.close()


def client():
    con = sqlite3.connect("capstone.db")
    con.execute("CREATE TABLE CLIENTS"
                "([generated_id] INTEGER PRIMARY KEY,"
                "[Client_Name] text,"
                "[Country_ID] integer,"
                "[Date] date)")

    print("Client table created")
    con.close()


def location():
    con = sqlite3.connect("capstone.db")
    con.execute('''CREATE TABLE COUNTRY
             ([generated_id] INTEGER PRIMARY KEY,
             [Country_ID] integer,
             [Country_Name] text)''')
    print("Location table created")
    con.close()


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


@app.route('/sign-up', methods=["POST"])
def sign_up():
    response = {}

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


@app.route('/location/', methods=["POST"])
# @jwt_required()
def insert_location():
    response = {}

    if request.method == "POST":
        generated_id = request.form['generated_id']
        Country_ID = request.form['Country_ID']
        Country_Name = request.form['Country_Name']

    with sqlite3.connect('capstone.db') as con:
        cursor = con.cursor()
        cursor.execute("INSERT INTO location("" ) VALUES(?, ?, ?)", (generated_id, Country_ID, Country_Name))
        con.commit()
        response["status_code"] = 201
        response['description'] = "Inserted location successfully"
        return response


if __name__ == '__main__':
    app.run(debug=True)
