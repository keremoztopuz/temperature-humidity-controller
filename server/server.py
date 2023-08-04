from flask import Flask , render_template,redirect,url_for,session,logging,request
from api import *
import argparse

from flask import Flask , render_template,redirect,url_for,session,logging,request
from api import *
import argparse

app = Flask(__name__)
app.secret_key = "XYXYXY"

data = {
    "device1": {
        "data": [
            {"date": "2023-08-01", "value": {}, "image": "", "alt": "Image 1"},
            {"date": "2023-08-02", "value": {}, "image": "", "alt": "Image 2"},
            {"date": "2023-08-03", "value": {}, "image": "", "alt": "Image 3"}
            # ... Diğer tarih verileri ...
        ]
    },
    "device2": {
        "data": [
            {"date": "2023-08-01", "value": {}, "image": "", "alt": "Image 4"},
            {"date": "2023-08-02", "value": {}, "image": "", "alt": "Image 5"},
            {"date": "2023-08-03", "value": {}, "image": "", "alt": "Image 6"}
            # ... Diğer tarih verileri ...
        ]
    }
}

# main site

@app.route("/", methods=["GET", "POST"])
def index():
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
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)
    