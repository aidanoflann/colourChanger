ColourChanger is a stupidly basic "MMO" game. The purpose is to log in and set the background of the website to your
colour. After a certain amount of time, the person who has had the background be set to their colour for the longest
wins.

The purpose of this project was to build a web-based game that implements usage of the following stack:

nginx webserver - uwsgi runners - python app - redis database

To get it running, follow these steps:

1) Run nginx with the following configuration in /etc/nginx/sites-enabled:
```
server {
        listen 8008;
        server_name doraboro.ddns.net;

        location / {
                include uwsgi_params;
                uwsgi_pass unix:/tmp/colourChanger.sock;
        }
}
```

2) Run a redis server with default config
```
redis-server
```

3) Initialise the uwsgi workers using a virtual environment with the requirements in requirements.txt installed:
```
uwsgi --ini colourChanger.ini -H linuxenv/
```

To instead run the project in a Docker container, follow these steps:

1) Run a redis container with basic configurations:
```
docker pull redis
docker run -p 6379:6379 --name my_redis redis
```

2) Build this project
```
docker build . -t cc
docker run
```

3) Run this project, with the required port (see nginx config) exposed. Link to the redis container by name
```
docker run --link my_redis:redis -p 8010:8010 -v C:\Users\Aidan\dev\colourChanger\colourChanger.py:/colourChanger.py cc
```