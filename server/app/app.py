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

global getURLMode
getURLMode = 0 # default mode
global getURLBySite
getURLBySite = ''

errorMessage = 'Error: Missing Information.'
failUpdate = 'Error: Database not updated. Was the site already added to the list?'
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
        for i in range(0,len(data)):
            for field in fields:
                get = data[i][field]
                
        return True
    except Exception as e:
        app.logger.info(str(e))
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
    
    app.logger.info(data)
    
    if isPass:
        result = insertTimeToDB(data)
        
        if result:
            app.logger.info('Data inserted')
            return 'Data inserted.'
        else:
            app.logger.info('Error reuslts is false')
            return errorMessage
    else:
        app.logger.info('Error with json')
        return errorMessage
        
@app.route('/getURL', methods=['GET'])
def getURL():
    level = '5'
    
    global getURLMode
    
    if getURLMode == 0:
        result = getURLFromDB(level)
    elif getURLMode == 1:
        global getURLBySite
        result = getURLWithSiteFromDB(level, getURLBySite)
    app.logger.info(result)
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
        return redirect(url_for("admin", noresults='No usable resources found on target website. Try another site?'))
        
@app.route('/getImages', methods=['GET'])
def getImgByName():
    #data = request.get_json()
    name = request.args.get('sitename', default = '', type = str)
    
    global getURLBySite
    
    if name is None:
        return errorMessage
    else:
        if name == "All":
            # default configuration
            getURLBySite = "All"
            return redirect(url_for("admin", isConfig=True))
        else:
            result = getImagesFromDB(name)
            if len(result) == 0:
                return redirect(url_for("admin", isConfig=False))
                
            getURLBySite = name
            
            global getURLMode
            getURLMode = 1
            return redirect(url_for("admin", isConfig=True))
    

@app.route('/getTiming', methods=['POST'])
def getTiming():
    data = request.get_json()
    #url = request.args.get('url', default = '', type = str)
    
    #app.logger.info(url)
    if data is None:
        return errorMessage
    else:
        url = data['sitename']
        app.logger.info(url)
        result = getTimeFromDB(url)
        return json.dumps(result, default=converter)

@app.route('/admin', methods=['GET'])
def admin():
    
    noresults = ''
    generateFail = ''
    generateSuccess = ''
    isConfig = False
    
    if 'generateFail' in request.args:
        generateFail = request.args['generateFail']
    elif 'generateSuccess' in request.args:
        generateSuccess = request.args['generateSuccess']
    elif 'noresults' in request.args:
        noresults = request.args['noresults']  
    elif 'isConfig' in request.args:
        isConfig = request.args['isConfig']
    
    imglist = getNameOfWebsiteFromDB()
    global getURLBySite
    
    return render_template("admin.html", imglist=imglist, generateFail=generateFail, generateSuccess=generateSuccess, noresults=noresults, isConfig=isConfig, sitemode=getURLBySite)

@app.route('/analysis', methods=['GET'])
@app.route('/analysis/<chart>/<threshold>', methods=['GET'])
@app.route('/analysis/<chart>/<threshold>', methods=['GET'])
def results(threshold=None, chart=None):

	if threshold is not None:
		threshold = int(threshold)

	if chart == "scatterplot":
		data = getPercentDiff(threshold)
	elif chart == "barchart":
		data = getNumberofSiteVists(threshold)

	if threshold is None:
		return render_template("analysis.html")
	elif 0 <= threshold < 100:
		
		resp = make_response(json.dumps(data))
		resp.headers['content-type'] = 'application/json'
		return resp
	else:
		return render_template("analysis.html")

@app.route('/experiment', methods=['GET'])
def showExperiment():
    data = getAllExperimentFromDB()
    return render_template("experiment.html", data=data)

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
    
