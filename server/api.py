from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import psycopg2

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

#cur.execute("CREATE TABLE person(name TEXT, age INT, height REAL)")
#cur.execute("INSERT INTO person(name, age, height) VALUES (%s, %s, %s)", ("Umut", 45, 199))

#READ FROM DATABASE
cur.execute("SELECT * FROM person")
rows = cur.fetchall()

for i in rows:
    print(i)

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