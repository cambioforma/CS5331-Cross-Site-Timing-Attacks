#!flask/bin/python
from typing import List, Dict
import mysql.connector
import datetime

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'CS5331'
}

def getNumberofSiteVists(threshold):
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor(prepared=True)

	cursor.execute('SELECT * FROM experiment')

	# extract row headers
	row_headers=[x[0] for x in cursor.description]
	rv = cursor.fetchall()
	json_data=[['Domain', 'Yes', 'No']]
	domainDict={}
	i=0

	for row in rv:
		_id = row[0]
		cookie = row[1].decode()
		url = row[2].decode()
		time1 = row[3]
		time2 = row[4]
		time3 = row[5]
		time4 = row[6]
		sitename = row[7].decode()
		currentDatetime = row[8]

		if time1>0:
			diff=(time1-(time2 + time3 + time4)/3)/time1

			if sitename in domainDict:
				if cookie in domainDict[sitename]:
					count = domainDict[sitename][cookie]
					if diff > (threshold/100):
						count[0] = count[0] + 1
						count[1] = count[1] + 1
					else:
						count[0] = count[0] + 1
					domainDict[sitename][cookie] = count
				else:
					if diff > (threshold/100):
						domainDict[sitename][cookie] = [1,1]
					else:
						domainDict[sitename][cookie] = [1,0]
			else:
				if diff > (threshold/100):
					domainDict[sitename] = {}
					domainDict[sitename][cookie] = [1,1]
				else:
					domainDict[sitename] = {}
					domainDict[sitename][cookie] = [1,0]

	for sitename, y in domainDict.items():
		total = 0
		yes = 0;
		for cookie, data in y.items():
			total = total + data[0]
			yes = yes + data[1]
		d = [sitename, total , total-yes]
		json_data.append(d)

	cursor.close()
	connection.close()

	return json_data

def getPercentDiff(threshold):
	connection = mysql.connector.connect(**config)
	cursor = connection.cursor(prepared=True)

	cursor.execute('SELECT * FROM experiment')

	# extract row headers
	row_headers=[x[0] for x in cursor.description]
	rv = cursor.fetchall()
	json_data=[]
	domainDict={}
	i=1;

	for row in rv:
		_id = row[0]
		cookie = row[1].decode()
		url = row[2].decode()
		time1 = row[3]
		time2 = row[4]
		time3 = row[5]
		time4 = row[6]
		sitename = row[7].decode()
		currentDatetime = row[8]

		if time1>0:
			diff=(time1-(time2 + time3 + time4)/3)/time1
			if (threshold is None) or (diff > (threshold/100)):
				experimentSet = sitename + cookie
				if sitename in domainDict:
					count = domainDict[experimentSet]
					count[0] = count[0] + 1
					count[1] = count[1] + diff
				else:
					domainDict[experimentSet] = [1, diff]
	
	for x, y in domainDict.items():
		d = [i, y[1]/y[0]]
		json_data.append(d)
		i = i + 1

	cursor.close()
	connection.close()

	return json_data

def getAllExperimentFromDB():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    cursor.execute('SELECT * FROM experiment')
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    
    for row in rv:
        _id = row[0]
        cookie = row[1].decode()
        url = row[2].decode()
        time1 = row[3]
        time2 = row[4]
        time3 = row[5]
        time4 = row[6]
        sitename = row[7].decode()
        currentDatetime = row[8]
        
        d = {
            'id': _id,
            'cookie': cookie,
            'url': url,
            'sitename': sitename.title(),
            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'currentDatetime': currentDatetime
        }
        
        json_data.append(d)
    
    cursor.close()
    connection.close()
    
    return json_data
    
def getTimeFromDB(url) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    cursor.execute('SELECT * FROM experiment where url = %s', (url,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    
    for row in rv:
        _id = row[0]
        cookie = row[1].decode()
        url = row[2].decode()
        time1 = row[3]
        time2 = row[4]
        time3 = row[5]
        time4 = row[6]
        sitename = row[7].decode()
        currentDatetime = row[8]
        
        d = {
            'id': _id,
            'cookie': cookie,
            'url': url,
            'time1': time1,
            'time2': time2,
            'time3': time3,
            'time4': time4,
            'sitename': sitename.title(),
            'currentDatetime': currentDatetime
        }
        
        json_data.append(d)
    
    cursor.close()
    connection.close()
    
    return json_data
    
def getSitenameFromURL(url):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT name FROM image where img_url = %s', (url,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    
    for row in rv:
        name = row[0].decode()
        #base_url = row[1].decode()
        #img_url = row[2].decode()
        
        return name
    
    cursor.close()
    connection.close()
    
    return None


def insertTimeToDB(data):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO experiment(cookie, url, time1, time2, time3, time4, sitename, currentDatetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    
    if len(data) < 4:
        return False
    else:
        try:
            url = data[0]['url']
            sitename = getSitenameFromURL(url)
            if sitename is None:
                sitename = 'ERROR'
            cookie = data[0]['cookie'].split('=')[1]
            value = (cookie, data[0]['url'], data[0]['time'], data[1]['time'], data[2]['time'], data[3]['time'], sitename, str(datetime.datetime.now()))
            cursor.execute(statement, value)
            connection.commit()
        except Exception as e:
            connection.close()
            return False
            
    connection.close()
    return True 
    

def getNameOfWebsiteFromDB():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT DISTINCT name FROM image LIMIT 10')
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    
    data=[]
    for row in rv:
        #name = row[0].decode()
        #base_url = row[1].decode()
        name = row[0].decode().title()
        
        data.append(name)
    
    cursor.close()
    connection.close()
    
    return data

def getImagesFromDB(name):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT * FROM image where name = %s', (name,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    
    data=[]
    for row in rv:
        #name = row[0].decode()
        #base_url = row[1].decode()
        img_url = row[2].decode()
        
        data.append(img_url)
    
    cursor.close()
    connection.close()
    
    return data
    

def insertImgToDB(base_url, name, images):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO image(name, base_url, img_url) VALUES (%s, %s, %s)"
    
    for link in images:
        try:
            value = (name, base_url, link)
            
            cursor.execute(statement, value)
            connection.commit()
        except Exception as e:
            print(str(e))
            return False
    
    connection.close()
    return True
    
def getURLFromDB(level):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    namelist = getNameOfWebsiteFromDB()
    data=[]
        
    for name in namelist:
        cursor.execute('SELECT img_url FROM image WHERE name = %s LIMIT %s', (name,level))
        
        # extract row headers
        row_headers=[x[0] for x in cursor.description]
        rv = cursor.fetchall()
        
        for row in rv:
            #name = row[0].decode()
            #base_url = row[1].decode()
            img_url = row[0].decode()
            data.append(img_url)
    
    cursor.close()
    connection.close()
    
    return data
    

def getURLWithSiteFromDB(level, site):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    data=[]
    
    cursor.execute('SELECT img_url FROM image WHERE name = %s LIMIT %s', (site,level))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    
    for row in rv:
        #name = row[0].decode()
        #base_url = row[1].decode()
        img_url = row[0].decode()
        data.append(img_url)

    cursor.close()
    connection.close()
    
    return data
    
