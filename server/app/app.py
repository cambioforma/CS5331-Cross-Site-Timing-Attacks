#!flask/bin/python
from typing import List, Dict
from flask import Flask, request, render_template
from scraper import getImages
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

@app.route('/', methods=['GET'])
def hello_test():
    return render_template("test.html")

errorMessage = 'Error: Missing Information.'
failUpdate = 'ERROR: Database not updated.'
successUpdate = 'SUCCESS: Database updated.'

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
    
def getImagesFromDB(name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT * FROM image where name = %s', (name,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    
    data=[]
    for row in rv:
        app.logger.info(row)
        #name = row[0].decode()
        #base_url = row[1].decode()
        img_url = row[2].decode()
        
        data.append(img_url)
    
    cursor.close()
    connection.close()
    
    return data
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        
def insertTimeToDB(data):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO timing(cookie, url, time, sequence) VALUES (%s, %s, %s, %s)"
    
    for key in data.keys():
        try:
            value = (data[key]['cookie'], data[key]['url'], data[key]['time'], data[key]['sequence'])
            
            cursor.execute(statement, value)
            connection.commit()
        except Exception as e:
            app.logger.info(e)
    connection.close()
    
def insertImgTODB(base_url, name, images):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO image(name, base_url, img_url) VALUES (%s, %s, %s)"
    
    for link in images:
        try:
            value = (name, base_url, link)
            
            cursor.execute(statement, value)
            connection.commit()
        except Exception as e:
            app.logger.info(e)
    
    connection.close()
    
def crawlURL(base_url, name):
    images = getImages(base_url)
    
    try:
        insertImgTODB(base_url, name, images)
        return True
    except Exception as e:
        app.logger.info(e)
        return False
     
    
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
        
@app.route('/addTiming', methods=['POST'])
def addTiming():
    data = request.get_json()
    
    isPass = checkJSONTiming(data)
    
    if isPass:
        insertTimeToDB(data)
        return 'Data inserted.'
    else:
        return errorMesssage
        
@app.route('/addImages', methods=['POST'])
def addImg():
    data = request.get_json()
    
    base_url = ''
    name = ''
    
    try:
        base_url = data['base_url'].lower()
        name = data['name'].lower()
        
        if base_url == '' or name == '':
            return 'Empty values are not accepted.'
        
        app.logger.info(base_url)
        app.logger.info(name)
    except Exception as e:
        app.logger.info(e)
        return 'Missing attribute. Ensure base_url and name are supplied.'
    
    isSuccess = crawlURL(base_url, name)
    
    if isSuccess:
        return successUpdate
        
    return failUpdate
    
@app.route('/getImages', methods=['GET'])
def getImgByName():
    name = request.args.get('name', default = '', type = str)
    
    if name == '':
        return errorMessage
    else:
        return json.dumps(getImagesFromDB(name), default=converter)
    

@app.route('/getTiming', methods=['GET'])
def getTiming():
    url = request.args.get('url', default = '', type = str)
    
    if url == '':
        return errorMessage
    else:
        return json.dumps(getTimeFromDB(url), default=converter)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
