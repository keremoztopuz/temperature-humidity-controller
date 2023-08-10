from flask import *
import argparse
from api import *

# main site

app = Flask(__name__)

@app.route("/api/getdata/<int:device_id>", methods=["GET"])
def getdata(device_id : int ):
    return api_getdata(device_id, args)

@app.route("/api/getcarddata", methods=["GET"])
def getcarddata():
    return api_getcarddata(args)

@app.route("/api/setdata/<int:device_id>/<float:temperature>/<float:humidity>", methods=["POST"])
def setdata(device_id: int, temperature: float, humidity: float):
    result = api_setdata(device_id, temperature, humidity, args)
    return result

@app.route("/api/getdevicelist", methods=["GET"])
def setdevicelist():
    return api_getdevicelist(args)

@app.route("/api/setdevicename/<int:device_id>/<string:device_name>", methods=["POST"])
def setdevicename(device_id: int, device_name: str):
    return api_setdevicename(device_id, device_name, args)

@app.route("/api/getgraph/<int:device_id>/<int:days_back>", methods=["GET"])
def getgraph(device_id : int, days_back: int ):
    return api_getgraph(device_id, days_back, args)

@app.route("/api/getgraphfull/<int:device_id>/<string:start_date>/<string:end_date>", methods=["GET"])
def getgraphfull(device_id: int, start_date: str, end_date: str):
    return api_getgraphfull(device_id, start_date, end_date, args)

@app.route("/")
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    parser.add_argument('--dbtype', type=str, default='postgresql', required=False, help='Database type. Eg: postgresql or mssql')
    parser.add_argument('--dbname', type=str, default='temperaturehumudity', required=False, help='Database name')
    parser.add_argument('--dbhost', type=str, default='localhost', required=False, help='Database host IP')
    parser.add_argument('--dbuser', type=str, default='postgres', required=False, help='Database username')
    parser.add_argument('--dbpassword', type=str, default='123456', required=False, help='Database user password')
    parser.add_argument('--dbport', type=str, default='5432', required=False, help='Database port')
    args = parser.parse_args()
    app.run(host=args.ip, port=args.port, debug=args.debug)