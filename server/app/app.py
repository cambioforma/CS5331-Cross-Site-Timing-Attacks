#!flask/bin/python
from typing import List, Dict
from flask import Flask, request
import mysql.connector
import json
import datetime
import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'CS5331'
}

errorMessage = 'Error: Missing Information.'


def getTimeFromDB(url) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT * FROM timing where url = %s', (url,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    for row in rv:
        app.logger.info(row)
        _id = row[0]
        cookie = row[1].decode()
        url = row[2].decode()
        time = row[3]
        sequence = row[4]
        
        d = {
            'id': _id,
            'cookie': cookie,
            'url': url,
            'time': time,
            'sequence': sequence
        }
        
        json_data.append(d)
    
    cursor.close()
    connection.close()
    
    return json_data
    
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        
def insertTimeToDB(data):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO timing(cookie, url, time, sequence) VALUES (%s, %s, %s, %s)"
    
    for key in data.keys():
        value = (data[key]['cookie'], data[key]['url'], data[key]['time'], data[key]['sequence'])
        
        cursor.execute(statement, value)
        connection.commit()
    
    connection.close()
    
def checkJSONTiming(data):
    keys = data.keys()
    
    fields = ['cookie', 'url', 'time', 'sequence']
    try: 
        for key in keys:
            for field in fields:
                get = data[key][field]
                
        return True
    except:
        return False
        
@app.route('/add', methods=['POST'])
def addTiming():
    data = request.get_json()
    
    isPass = checkJSONTiming(data)
    
    if isPass:
        insertTimeToDB(data)
        return 'Data inserted.'
    else:
        return errorMesssage

@app.route('/getTiming', methods=['GET'])
def getTiming():
    url = request.args.get('url', default = '', type = str)
    
    if url == '':
        return errorMessage
    else:
        return json.dumps(getTimeFromDB(url), default=converter)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
