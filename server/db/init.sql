CREATE DATABASE CS5331;
use CS5331;

CREATE TABLE experiment
(
id INT NOT NULL AUTO_INCREMENT,
cookie VARCHAR(64) NOT NULL,
url VARCHAR(1024) NOT NULL,
time1 INT NOT NULL,
time2 INT NOT NULL,
time3 INT NOT NULL,
time4 INT NOT NULL,
timediff FLOAT(7,4) NOT NULL,
currentDatetime TIMESTAMP NOT NULL,
PRIMARY KEY(id)
);

CREATE TABLE image
(
name VARCHAR(64) NOT NULL, 
base_url VARCHAR(64) NOT NULL,
img_url VARCHAR(1024) NOT NULL,
PRIMARY KEY(name, img_url)
);

INSERT INTO experiment(cookie, url, time1, time2, time3, time4, timediff, currentDatetime) 
VALUES ('COOKIEVALUE', 'test.com', '10', '2', '3', '5', '0.9', '2019-01-01 12:12:12');
 
