#!/bin/bash
service nginx start
uwsgi --ini colourChanger.ini &
tail -f /var/log/nginx/access.log
