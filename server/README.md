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

When refreshing database:
- Execute `docker-compose rm -fv db` to refresh the database after stopping the docker image. 
