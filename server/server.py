from flask import Flask , render_template,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from api import *
import argparse

app = Flask(__name__)
app.secret_key = "XYXYXY"

valid_users = {
    "demo_user": "demo_password",
    "test_user": "test_password"
}

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "oguzarduc" and password == "mauroicardi99":
            session['logged_in'] = True  # Set the session variable to indicate successful login
            return redirect(url_for("index"))
        else:
            error = "Invalid username or password. Please try again."

    return render_template("login.html", error=error)


# main site

@app.route("/")
def index():
    if 'logged_in' in session:
        return render_template("index_logged_in.html")
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop('logged_in', None) 
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if 'logged_in' in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    