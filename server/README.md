# Server Instructions

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

timing(cookie, url, time, sequence)

## Insert to Database

### Timing
Use POST method and supply the timing details in the form of JSON. 
Example using curl:
`curl --header "Content-Type: application/json" --request POST --data '{"0":{"cookie":"c000kie","url":"hello.com","time":"60","sequence":0},"1":{"cookie":"c000kie","url":"hello.com","time":"30","sequence":1},"2":{"cookie":"c000kie","url":"hello.com","time":"22","sequence":2},"3":{"cookie":"c000kie","url":"hello.com","time":"25","sequence":3}}' http://127.0.0.1:5000/addTiming`

### Image resource links
Use POST method and supply the base_url and name of website in the form of JSON.
Example using curl:
`curl --header "Content-Type: application/json" --request POST --data '{"base_url": "https://www.facebook.com", "name":"facebook"}' http://127.0.0.1:5000/addImages`

## Query from Database
### Timing
`http://127.0.0.1:5000/getTiming?url=<VALUE>`

### Images
`http://127.0.0.1:5000/getImages?name=<VALUE>`

