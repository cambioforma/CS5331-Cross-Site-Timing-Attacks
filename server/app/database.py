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
def getResultsFromDB():
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
		currentDatetime = row[7]

		diff=(time1-(time2 + time3 + time4)/3)/time1
		d = [_id, diff]
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
        currentDatetime = row[7]
        
        d = {
            'id': _id,
            'cookie': cookie,
            'url': url,
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
        name = row[0].decode()
        
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
    
def insertTimeToDB(data):
    connection = mysql.connector.connect(**config)
    
    cursor = connection.cursor(prepared=True)
    statement = "INSERT INTO experiment(cookie, url, time1, time2, time3, time4, currentDatetime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    if len(data) < 4:
        return False
    else:
        try:
            value = (data[0]['cookie'], data[0]['url'], data[0]['time'], data[1]['time'], data[2]['time'], data[3]['time'], str(datetime.datetime.now()))
            cursor.execute(statement, value)
            connection.commit()
        except Exception as e:
            print(str(e))
            return False
    connection.close()
    return True   
    
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
            print(str(e))
    
    connection.close()
    
    