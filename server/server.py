from flask import Flask , render_template
import argparse
from api import *

app = Flask(__name__)
@app.route("/")
def index():
    return "Hello HTML"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print('Hello,', args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    
    #332211