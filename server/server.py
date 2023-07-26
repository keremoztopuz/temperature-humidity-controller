from flask import Flask , render_template,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from api import *
import argparse

app = Flask(__name__)

valid_users = {
    "demo_user": "demo_password",
    "test_user": "test_password"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in valid_users and valid_users[username] == password:
            return redirect(url_for("welcome", username=username))
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template("login.html", error=error_message)

    return render_template("login.html")

@app.route("/welcome/<username>")
def welcome(username):
    return "welcome user"

mysql = MySQL(app)

# main site

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    