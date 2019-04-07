CREATE DATABASE CS5331;
use CS5331;

CREATE TABLE timing
(
id INT NOT NULL AUTO_INCREMENT,
cookie VARCHAR(64) NOT NULL,
url VARCHAR(64) NOT NULL,
time INT NOT NULL,
sequence INT NOT NULL,
currentDatetime TIMESTAMP NOT NULL,
PRIMARY KEY(ID)
);

CREATE TABLE image
(
name VARCHAR(64) NOT NULL, 
base_url VARCHAR(64) NOT NULL,
img_url VARCHAR(64) NOT NULL,
PRIMARY KEY(name, img_url)
);

INSERT INTO timing(cookie, url, time, sequence)
VALUES ('COOKIEVALUE', 'test.com', '10', 2);
 
