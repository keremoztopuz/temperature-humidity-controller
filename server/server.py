from flask import Flask , render_template, request , jsonify
import argparse
from api import *

# main site

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/api/getdata/<int:device_id>", methods=["GET"])
def getdata(device_id : int ):
    return api_getdata(device_id)

@app.route("/api/setdata/<int:device_id>/<float:temperature>", methods=["POST"])
def setdata(device_id : int , temperature : float):
    data = api_setdata(device_id, temperature)
    return jsonify(data)

@app.route("/api/setdevicelist", methods=["POST"])
def setdevicelist():
    return api_setdevicelist()

@app.route("/api/setdevicename/<int:device_id>/<string:name>", methods=["POST"])
def setdevicename(device_id : int , name : str):
    return api_setdevicename(device_id, name)

@app.route("/api/getgraph/<int:device_id>", methods=["GET"])
def getgraph(device_id : int ):
    return api_getgraph(device_id)

@app.route("/api/getgraphfull/<int:device_id>/<string:start_date>/<string:end_date>", methods=["GET"])
def getgraphfull(device_id : int , start_date : int , end_date : int):
    return api_getgraphfull(device_id, start_date, end_date)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)