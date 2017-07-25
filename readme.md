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