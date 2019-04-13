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
failUpdate = 'Error: Database not updated.'
successUpdate = 'Success: Database updated.'

    
def converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        
def scrape(base_url, name):
    images = getImages(base_url)
        
    try:
        result = insertImgToDB(base_url, name, images)
        if result is True:
            return images
        else:
            return None
    except Exception as e:
        app.logger.info(e)
        return None
     
def checkJSONTiming(data):
    
    fields = ['url', 'time', 'cookie']
    try: 
        for i in len(data):
            for field in fields:
                get = data[i][field]
                
        return True
    except:
        return False

def isNone(data):
    if data is None:
        return True
    else:
        return False

@app.route('/', methods=['GET'])
def index():
	resp = make_response(render_template("index.html"))
	if 'userId' in request.cookies:
		user = request.cookies.get('userId')
	else:
		uid = random.randint(1,2**64)
		resp.set_cookie('userId', str(uid))

	return resp

@app.route('/addTiming', methods=['POST'])
def addTiming():
    data = request.get_json()
    
    if data is None:
        return errorMessage
    
    isPass = checkJSONTiming(data)
    isPass = True
    if isPass:
        result = insertTimeToDB(data)
        if result:
            return 'Data inserted.'
        else:
            return errorMessage
    else:
        return errorMessage
        
@app.route('/getURL', methods=['GET'])
def getURL():
    level = '5'
    result = getURLFromDB(level)
    return json.dumps(result)
        
@app.route('/addImages', methods=['POST'])
def addImg():
    data = request.form.to_dict(flat=False)
    app.logger.info(data)
    base_url = ''
    name = ''
    
    try:
        base_url = data['base_url'][0].lower()
        name = data['name'][0].lower()
        
        if base_url == '' or name == '':
            return redirect(url_for("admin", generateFail='Empty values are not accepted.'))
        
    except Exception as e:
        app.logger.info(e)
        return redirect(url_for("admin", generateFail='Missing attribute. Ensure base_url and name are supplied.'))
    
    images = scrape(base_url, name)
    
    if images is None:
        return redirect(url_for("admin", generateFail=failUpdate))
    elif len(images) > 0:
        return redirect(url_for("admin", generateSuccess=successUpdate))
    else:
        return redirect(url_for("admin", noresults='No resources found on target website.'))

@app.route('/getImages', methods=['GET'])
def getImgByName():
    #name = request.args.get('name', default = '', type = str)
    name = request.args.get('sitename', default = '', type = str)
    
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
        result = getTimeFromDB(url)
        return json.dumps(result, default=converter)

@app.route('/admin', methods=['GET'])
def admin():
    noresults = ''
    generateFail = ''
    generateSuccess = ''
    
    if 'generateFail' in request.args:
        generateFail = request.args['generateFail']
    if 'generateSuccess' in request.args:
        generateSuccess = request.args['generateSuccess']
    if 'noresults' in request.args:
        noresults = request.args['noresults']
    
    imglist = getNameOfWebsiteFromDB()
    return render_template("admin.html", imglist=imglist, generateFail=generateFail, generateSuccess=generateSuccess, noresults=noresults)

@app.route('/results', methods=['GET'])
@app.route('/results/<threshold>', methods=['GET'])
def results(threshold=None):
	data = getResultsFromDB()

	if threshold is None:
		return render_template("results.html", data=json.dumps(data))
	elif threshold=="data":
		resp = make_response(json.dumps(data))
		resp.headers['content-type'] = 'application/json'
		return resp
	else:
		return render_template("results.html", data=json.dumps(data))

@app.route('/initdb', methods=['GET'])
def init_db():
    scrape('https://goodyfeed.com/', 'goodyfeed')
    scrape('https://www.facebook.com/', 'facebook')
    scrape('https://stackoverflow.com', 'stackoverflow')
    scrape('https://www.boredpanda.com/', 'bored panda')
    scrape('https://www.straitstimes.com/', 'the straits times')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
