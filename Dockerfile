FROM 364843010988.dkr.ecr.eu-west-1.amazonaws.com/base_python:master
MAINTAINER Aidan OFlannagain

ADD . .

RUN apt-get update
RUN apt-get install -y redis-server uwsgi-core uwsgi-plugin-python nginx
RUN pip install --upgrade -r requirements.txt

ADD nginx_config/sites-available/* /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/colourChanger /etc/nginx/sites-enabled/colourChanger

CMD sh start.sh