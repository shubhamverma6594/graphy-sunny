from flask import Flask
from routes import routes
import logging
from logging import Formatter, FileHandler
import os
import json_log_formatter
import mysql.connector
from mysql.connector import Error
from constant import Commons
from async import Consumer, process_message
import importlib.util

app = Flask(__name__)
app.register_blueprint(routes)

app.debug = True
app.config['DATABASE_NAME'] = 'library.db'

formatter = json_log_formatter.JSONFormatter()
json_handler = logging.FileHandler(filename='.ot-python-api.json')
json_handler.setFormatter(formatter)

spec = importlib.util.spec_from_file_location("module.name", "./config/local.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

def load_mysql_connector():
    try:
        mydb = mysql.connector.connect(
            host="18.224.229.26",
            database='graphy',
            user="graphy",
            passwd="12345"
        )
    except Error as e:
        print("Error getting mysql connection", e)
    Commons.mysql = mydb
    print("in starting " , mydb)

def start_rabbit():
    print("Starting rabbit consumer")
    image_process_request_consumer = Consumer(config.image_process_request_config, config.mq_config)

    image_process_request_consumer.consume(process_message)
    print("Started rabbit consumer")

load_mysql_connector()
start_rabbit()

if __name__ == '__main__':
    host = os.environ.get('IP', '127.0.0.1')
    port = int(os.environ.get('PORT', 80))
    app.run(host=host, port=port, debug=False)
