#!flask/bin/python
from typing import List, Dict
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'CS5331'
}


def getTimeFromDB(url) -> List[Dict]:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(prepared=True)
    
    cursor.execute('SELECT * FROM timing where url = %s', (url,))
    
    # extract row headers
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    
    for row in rv:
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
            print(str(e))
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
            print(str(e))
    
    connection.close()
    
    
