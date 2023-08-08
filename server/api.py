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
from datetime import datetime

def api_getdata(device_id: int, dbtype: str):
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()
        # Veriyi sorgulama işlemi
        if dbtype == "postgresql":
            query = "SELECT * FROM devicedatas WHERE device_id = %s ORDER BY data_date desc LIMIT 1;" 
        elif dbtype == "mssql":
            query = "SELECT TOP 1 * FROM devicedatas WHERE device_id = %s ORDER BY data_date desc ;" 
        else:
            return
        cursor.execute(query, (device_id,))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        # Sorgulanan veriyi JSON olarak döndürme
        result = []
        for row in data:
            result.append({
                'device_id': row[0],
                'data_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': row[2],
                'humidity': row[3]
            })

        return jsonify({"data": result})

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error while fetching data: ' + str(e)
        })

# PostgreSQL veritabanına veri eklemek için işlev
def api_setdata(device_id, temperature, humidity):
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        # Verileri ekleme işlemi
        insert_query = "INSERT INTO devicedatas (device_id, data_date, temperature, humidity) VALUES (%s, %s, %s, %s);"
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
        return jsonify({
            'status': 'error',
            'message': 'Data could not be added, try again: ' + str(e)
        })

def api_getdevicelist():
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        # Cihazları sorgulama işlemi
        query = "SELECT * FROM devices;"
        cursor.execute(query)
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        # Sorgulanan cihaz verilerini JSON olarak döndürme
        devices = []
        for row in data:
            devices.append({
                'id': row[0],
                'name': row[1]
            })

        return jsonify({
            'status': 'ok',
            'message': 'Device list retrieved successfully',
            'devices': devices
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error while retrieving device list: ' + str(e)
        })

def api_setdevicename(device_id, device_name):
    try:
        # Veritabanına bağlanma
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        # Veritabanında cihazın olup olmadığını kontrol etme
        check_query = "SELECT COUNT (*) FROM devices WHERE device_id = %s;"
        cursor.execute(check_query, (device_id,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Cihaz yoksa ekleme işlemi
            insert_query = "INSERT INTO devices (device_id, device_name) VALUES (%s, %s);"
            cursor.execute(insert_query, (device_id, device_name))
        else:
            # Cihaz varsa güncelleme işlemi
            update_query = "UPDATE devices SET device_name = %s WHERE device_id = %s;"
            cursor.execute(update_query, (device_name, device_id))

        connection.commit()  # Veritabanında değişiklikleri kaydetme
        cursor.close()  # Cursor kapatma
        connection.close()  # Veritabanı bağlantısını kapatma

        if count == 0:
            return jsonify({
                'status': 'ok',
                'message': 'Device successfully inserted'
            })
        else:
            return jsonify({
                'status': 'ok',
                'message': 'Device name updated successfully'
            })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error while updating device name: ' + str(e)
        })


def api_getgraph(device_id: int, days_back: int):
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        # Veriyi sorgulama işlemi
        query = "SELECT data_date, temperature, humidity FROM devicedatas WHERE device_id = %s AND data_date >= now() - interval %s ORDER BY data_date;"
        cursor.execute(query, (device_id, f"{days_back} days"))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        # Sorgulanan veriyi JSON olarak döndürme
        result = []
        for row in data:
            result.append({
                'data_date': row[0].strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': row[1],
                'humidity': row[2]
            })

        return jsonify({"data": result})

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error while fetching data for graph: ' + str(e)
        })

def api_getgraphfull(device_id: int, start_date: str, end_date: str):
    try:
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=5433
        )
        cursor = connection.cursor()

        query = "SELECT * FROM devicedatas WHERE device_id = %s AND data_date >= %s AND data_date <= %s ORDER BY data_date;"
        cursor.execute(query, (device_id, start_date, end_date))
        data = cursor.fetchall()

        cursor.close()
        connection.close()

        result = []
        for row in data:
            result.append({
                'device_id': row[0],
                'data_date': str(row[1]),  # str() fonksiyonunu kullanarak tarih verisini string olarak döndürme
                'temperature': row[2],
                'humidity': row[3]
            })

        return jsonify({"data": result})

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error while fetching data: ' + str(e)
        })

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)