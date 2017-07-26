#!/bin/bash
service nginx start
redis-server &
uwsgi --ini colourChanger.ini &
tail -f /var/log/nginx/access.log
