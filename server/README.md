# Server Instructions

To start with some examples, access 127.0.0.1:5000/initdb. 

## Server: Flask
Install docker.io and docker-compose.

To start the server, execute the commands at git root directory (`/CS5331-Cross-Site-Timing-Attacks/`):
1. `docker-compose build`
2. `docker-compose up`
3. Web server can be found at `localhost:5000` or `127.0.0.1:5000`

If you prefer using without the logging info, use `docker-compose up -d` instead.

To stop, either Ctr-C or `docker-compose stop`. 

## Database: MySQL
The database can be found at `mysql --host=127.0.0.1 --port=32000 -u root -p`
Password is `root`. 

Common commands:
1. `use CS5331`
2. `show tables`

When refreshing database:
- Execute `docker-compose rm -fv db` after stopping the docker image. 

## Database Tables:

experiment(id, cookie, url, time1, time2, time3, time4, sitename, currentDatetime)

image(name, base_url, img_url)

## Insert to Database

### Timing
Use POST method and supply the timing details in the form of JSON. 
Example using curl:
`curl --header "Content-Type: application/json" --request POST --data '{"0":{"cookie": "userId=123abc", "url":"hello.com","time":"60"},"1":{"cookie": "userId=123abc", "url":"hello.com","time":"30"},"2":{"cookie": "userId=123abc", "url":"hello.com","time":"22"},"3":{"cookie": "userId=123abc", "url":"hello.com","time":"25"}}' http://127.0.0.1:5000/addTiming -v`

### Image resource links
Use POST method and supply the base_url and name of website in the form of JSON.
Example using curl:
`curl --header "Content-Type: application/json" --request POST --data '{"base_url": "https://www.facebook.com", "name":"facebook"}' http://127.0.0.1:5000/addImages`

## Query from Database
### Timing
`http://127.0.0.1:5000/getTiming?url=<VALUE>`

`curl --header "Content-Type: application/json" --request POST --data '{"sitename":"<VALUE>"}' http://127.0.0.1:5000/getTiming`

### Images
`http://127.0.0.1:5000/getImages?name=<VALUE>`

