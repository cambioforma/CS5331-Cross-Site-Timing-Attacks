#!flask/bin/python
from typing import List, Dict
from flask import Flask
import mysql.connector
import json
import datetime

app = Flask(__name__)


def timing() -> List[Dict]:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'CS5331'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM timing')
    row_headers=[x[0] for x in cursor.description] #this will extract row headers
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()
    connection.close()
    return json.dumps(json_data, default=converter)
    
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

@app.route('/')
def index() -> str:
    return timing()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
