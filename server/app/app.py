#!flask/bin/python
from typing import List, Dict
from flask import Flask, request, render_template, make_response, redirect, url_for
from scraper import getImages
from database import *
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
    
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        
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
        result = getImagesFromDB(name)
        if len(result) == 0:
            return "No results found"
        return json.dumps(result)
    

@app.route('/getTiming', methods=['GET'])
def getTiming():
    url = request.args.get('url', default = '', type = str)
    
    if url == '':
        return errorMessage
    else:
        return json.dumps(getTimeFromDB(url), default=converter)

@app.route('/admin', methods=['GET'])
def admin():
    imglist = getNameOfWebsiteFromDB()
    return render_template("admin.html", imglist=imglist)

@app.route('/results', methods=['GET'])
def results():
	return render_template("results.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
