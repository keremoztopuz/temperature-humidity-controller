from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import psycopg2
import json
from datetime import datetime
import http.client
import argparse

app = Flask(__name__)
api = Api(app)

class GetData:
    def __init__(self, device_id, data_date, conn):
        self.device_id = device_id
        self.data_date = data_date
        self.conn = conn

    def insert_data(self):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO devicedatas(device_id, data_date) VALUES (%s, %s)",
                    (self.device_id, self.data_date))
        cur.execute("INSERT INTO devices(device_id, device_name) VALUES (%s, %s)",
                    (self.device_id, request.args.get('device_name')))  

        self.conn.commit()
        cur.close()

    def get_device_list(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM devicedatas JOIN devices ON devicedatas.device_id = devices.device_id")
        rows = cur.fetchall()

        data_list = []
        for row in rows:
            data_dict = {
                'data_id': row[0],
                'device_id': row[1],
                'data_date': row[2].strftime('%Y-%m-%d %H:%M:%S'),
                'device_name': row[4]
            }
            data_list.append(data_dict)

        json_data = json.dumps(data_list, indent=4)
        cur.close()

        return json_data

def api_getdata(device_id: int):
    conn = psycopg2.connect(
        host="localhost",
        database="temperaturehumidity",
        password="123456",
        user="postgres"
    )

    try:
        initial_date = datetime.now()
        added_date = initial_date

        data_handler = GetData(device_id, added_date, conn)
        data_handler.insert_data()

        return jsonify({"message": f"Data for device {device_id} inserted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()


def api_getdevicelist():
    conn = psycopg2.connect(
        host="localhost",
        database="temperaturehumidity",
        password="123456",
        user="postgres"
    )

    device_id = 1  
    data_date = datetime.now()  

    data_handler = GetData(device_id, data_date, conn)
    json_data = data_handler.get_device_list()

    return jsonify(json.loads(json_data))

    """
    with open('output.json','w') as file:
        file.write(json_data)

    try:
        with open('output.json', 'r') as file:
            data_list = json.load(file)
            return json.dumps(data_list)
    except FileNotFoundError:
        return "Data not available."
    except Exception as e:
        return f"An error occurred: {str(e)}
    """
    
def api_setdevicename(device_id , name):
    api_host = "localhost"
    api_port = 5000
    api_path = f"/api/setdevicename/{device_id}/{name}"

    try:
        connection = http.client.HTTPConnection(api_host, api_port)
        headers = {'Content-type': 'application/json'}

        connection.request("POST", api_path, headers=headers)
        response = connection.getresponse()

        response_data = json.loads(response.read().decode())

        connection.close()

        if response.status == 200:
            return response_data
        else:
            return {"error": f"Failed to update device name. Status code: {response.status}"}
    except Exception as e:
        return {"error": str(e)}

def api_setdata(device_id, temperature):
    conn = psycopg2.connect(
        host="localhost",
        database="temperaturehumidity",
        password="123456",
        user="postgres"
    )

    try:
        data_date = datetime.now()
        cur = conn.cursor()
        cur.execute("INSERT INTO devicedatas (device_id, data_date, temperature) VALUES (%s, %s, %s)",
                    (device_id, data_date, temperature))
        conn.commit()
        cur.close()

        return jsonify({"message": f"Data for device {device_id} set successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

def api_getgraph(device_id):
    conn = psycopg2.connect(
        host="localhost",
        database="temperaturehumidity",
        password="123456",
        user="postgres"
    )

    try:
        cur = conn.cursor()
        cur.execute("SELECT data_date, temperature FROM devicedatas WHERE device_id = %s", (device_id,))
        rows = cur.fetchall()
        cur.close()

        data_list = []
        for row in rows:
            data_dict = {
                'data_date': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': row[1]
            }
            data_list.append(data_dict)

        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()


def api_getgraphfull(device_id, start_date, end_date):
    conn = psycopg2.connect(
        host="localhost",
        database="temperaturehumidity",
        password="123456",
        user="postgres"
    )

    try:
        cur = conn.cursor()
        cur.execute("SELECT data_date, temperature FROM devicedatas WHERE device_id = %s AND data_date BETWEEN %s AND %s",
                    (device_id, start_date, end_date))
        rows = cur.fetchall()
        cur.close()

        data_list = []
        for row in rows:
            data_dict = {
                'data_date': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': row[1]
            }
            data_list.append(data_dict)

        return jsonify(data_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)


