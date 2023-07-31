from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2
import json
from datetime import datetime


app = Flask(__name__)
api = Api(app)

conn = psycopg2.connect(
    host="localhost",
    database="temperaturehumidity",
    password="123456",
    user = "postgres"
    )

print("Connection Successful")

cur = conn.cursor()

initial_date = datetime.now()
added_date = initial_date

cur.execute("INSERT INTO devicedatas(data_id, device_id, data_date) VALUES (%s, %s, %s)", (int(input("data_id:")), int(input("device_id:")) , added_date))
cur.execute("INSERT INTO devices(device_id, device_name) VALUES (%s, %s)", (int(input("device_id:")), str(input("device_name:"))))

#READ FROM DATABASE
cur.execute("SELECT * FROM devicedatas")
rows = cur.fetchall()

data_list = []
for row in rows:
    data_dict = {
        'data_id': row[0],
        'device_id': row[1],
        'data_dates': row[2].strftime('%Y-%m-%d %H:%M:%S')
    }
    data_list.append(data_dict)

json_data = json.dumps(data_list)
print(json_data)

#OPEN DATABASE
with open('output.json', 'w') as file:
    file.write(json_data)

conn.commit()
conn.close()



def api_getdata(device_id):
    return "api_getdata:" + " " + str(device_id)

def api_setdata(device_id , temperature):
    return "api_setdata:" + str(device_id) + " " + str(temperature)

def api_getdevicelist(getdevlist):
    return "api_getdevicelist:" + " " + str(getdevlist)

def api_setdevicename(device_id , name):
    return "api_setdevicename:" + " " + str(device_id) + " " + name

def api_getgraph(device_id):
    return "api_getgraph:" + " " + str(device_id)

def api_getgraphfull(device_id, start_date, end_date):
    return "api_getgraphfull:" + " " + str(device_id) + " " + str(start_date) + " " + str(end_date)