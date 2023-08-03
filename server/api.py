from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import psycopg2
import json
from datetime import datetime
import http.client
import argparse

app = Flask(__name__)

def api_getdata(device_id):
    return "api_getdata:" + " " + str(device_id)

def api_setdata(device_id, temperature, humidity):
    return "api_setdata:" + " " + str(device_id, temperature, humidity)

def api_setdevicelist():
    return "api_setdevicelist:" + " " 

def api_setdevicename(device_id, device_name):
    return "api_setdevicename:" + " " + str(device_id) + " " + device_name

def api_getgraph(device_id):
    return "api_getgraph:" + " " + str(device_id)

def api_getgraphfull(device_id, start_date, end_date):
    return "api_getgraphfull:" + " " + str(device_id) + " " + str(start_date) + " " + str(end_date)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="server")
    parser.add_argument('--debug', action='store_true', required=False, help='Enable debug mode')
    parser.add_argument('--port', type=int, default=5000, required=False, help='Port number (default: 5000)')
    parser.add_argument('--ip', type=str, default='127.0.0.1', required=False, help='IP address (default: 127.0.0.1)')
    args = parser.parse_args()
    print(args.debug)
    app.run(host=args.ip, port=args.port, debug=args.debug)


