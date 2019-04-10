#!flask/bin/python
from typing import List, Dict
from flask import Flask, request, render_template, make_response, redirect, url_for
from scraper import getImages
import mysql.connector
import json
import datetime
import logging
import random
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
failUpdate = 'ERROR: Database not updated.'
successUpdate = 'SUCCESS: Database updated.'

@app.route('/', methods=['GET'])
def index():
	resp = make_response(render_template("index.html"))
	if 'userId' in request.cookies:
		user = request.cookies.get('userId')
	else:
		uid = random.randint(1,2**64)
		resp.set_cookie('userId', str(uid))

	return resp

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
        currentDatetime = row[5]
        
        d = {
            'id': _id,
            'cookie': cookie,
            'url': url,
            'time': time,
            'sequence': sequence,
            'currentDatetime': currentDatetime
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
        
def insertTimeToDB(data, cookie):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO timing(cookie, url, time, sequence, currentDatetime) VALUES (%s, %s, %s, %s, %s)"
    
    seq = 0
    for key in data.keys():
        try:
            value = (cookie, data[key]['url'], data[key]['time'], seq, str(datetime.datetime.now()))
            seq = seq + 1
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
    
    fields = ['url', 'time']
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
    
    cookie = ''
    if 'userId' in request.cookies:
	    cookie = request.cookies.get('userId')
    else:
        return redirect(url_for('index'))
    
    isPass = checkJSONTiming(data)
    
    if isPass:
        insertTimeToDB(data, cookie)
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
        return json.dumps(getImagesFromDB(name))
    

@app.route('/getTiming', methods=['GET'])
def getTiming():
    url = request.args.get('url', default = '', type = str)
    
    if url == '':
        return errorMessage
    else:
        return json.dumps(getTimeFromDB(url), default=converter)

@app.route('/admin', methods=['GET'])
def admin():
	return render_template("admin.html")

@app.route('/results', methods=['GET'])
def results():
	return render_template("results.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
