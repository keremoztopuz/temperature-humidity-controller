from flask import Flask , render_template,redirect,url_for,session,logging,request
from api import *, request , jsonify
import argparse

from flask import Flask , render_template,redirect,url_for,session,logging,request
from api import *
import argparse

# main site

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/api/getdata/<int:device_id>", methods=["GET"])
def getdata(device_id : int ):
    return api_getdata(device_id, args.dbtype)

@app.route("/api/setdata/<int:device_id>/<float:temperature>/<float:humidity>", methods=["POST"])
def setdata(device_id: int, temperature: float, humidity: float):
    result = api_setdata(device_id, temperature, humidity)
    return result

@app.route("/api/getdevicelist", methods=["GET"])
def setdevicelist():
    return api_getdevicelist()

@app.route("/api/setdevicename/<int:device_id>/<string:device_name>", methods=["POST"])
def setdevicename(device_id: int, device_name: str):
    return api_setdevicename(device_id, device_name)

@app.route("/api/getgraph/<int:device_id>/<int:days_back>", methods=["GET"])
def getgraph(device_id : int, days_back: int ):
    return api_getgraph(device_id, days_back)

@app.route("/api/getgraphfull/<int:device_id>/<string:start_date>/<string:end_date>", methods=["GET"])
def getgraphfull(device_id: int, start_date: str, end_date: str):
    return api_getgraphfull(device_id, start_date, end_date)
    error_message = ""
    chart_data = []

    if request.method == "POST":
        start_date = request.form.get("startDate")
        end_date = request.form.get("endDate")
        selected_device = request.form.get("device")

        if not start_date or not end_date or not selected_device:
            error_message = "Lütfen tarih aralığı ve cihaz seçimini doldurun."
        else:
            chart_data = data.get(selected_device, {}).get("data", [])
            chart_data = [item for item in chart_data if start_date <= item["date"] <= end_date]

    return render_template("index.html", error_message=error_message, chart_data=chart_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    parser.add_argument('--dbtype', type=str, default='postgresql', required=False, help='Database type. Eg: postgresql or mssql')
    args = parser.parse_args()
    print('Hello,', args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    
    #332211