#!flask/bin/python
from typing import List, Dict
from flask import Flask, request
import mysql.connector
import json
import datetime

app = Flask(__name__)

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'CS5331'
}

def timing(url) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT * FROM timing where url = %s', (url,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description] 
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

@app.route('/getTiming', methods=['GET'])
def index():
    url = request.args.get('url', default = '', type = str)
    
    if url == '':
        return 'Error. Please supply url'
    else:
        return timing(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
