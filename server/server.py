from flask import Flask , render_template
import argparse
from api import *

# main site

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/temperature")
def temperature():
    return render_template("temperature.html")

@app.route("/squares")
def click():
    return render_template("squares.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    