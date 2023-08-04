from flask import Flask, request, jsonify
import psycopg2
import http.client
import argparse
from datetime import datetime

app = Flask(__name__)

# PostgreSQL veritabanı bağlantısı için gerekli bilgileri doldurun
db_host = "localhost"
db_name = "temperaturehumudity"
db_user = "postgres"
db_password = "123456"


# API endpoint'leri
def api_getdata(device_id):
    return jsonify({"data": "api_getdata: " + str(device_id)})

# PostgreSQL veritabanına veri eklemek için işlev
def api_setdata(device_id, temperature, humidity):
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        # Verileri ekleme işlemi
        insert_query = "INSERT INTO devicedatas (device_id, datetime, temperature, humidity) VALUES (%s, %s, %s, %s);"
        current_datetime = datetime.now()
        cursor.execute(insert_query, (device_id, current_datetime, temperature, humidity))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({
            'status': 'ok',
            'message': 'Data added successfully'
            })

    except Exception as e:
        return ({
            'status' : 'error',
            'message': 'Data could not add try again ' + str(e)
            })

def api_setdevicelist():
    return jsonify({"data": "api_setdevicelist"})

def api_setdevicename():
    data = request.json
    device_id = data.get("device_id")
    device_name = data.get("device_name")
    return jsonify({"data": "api_setdevicename: " + str(device_id) + " " + device_name})

def api_getgraph(device_id):
    return jsonify({"data": "api_getgraph: " + str(device_id)})

def api_getgraphfull(device_id, start_date, end_date):
    return jsonify({"data": "api_getgraphfull: " + str(device_id) + " " + start_date + " " + end_date})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)