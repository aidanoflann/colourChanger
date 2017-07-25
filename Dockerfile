FROM 364843010988.dkr.ecr.eu-west-1.amazonaws.com/base_python:master
MAINTAINER Aidan OFlannagain

ADD . .

RUN apt-get update
RUN apt-get install -y redis-server uwsgi-core uwsgi-plugin-python nginx
RUN pip install --upgrade -r requirements.txt

CMD service nginx start
CMD redis-server
CMD uwsgi --ini colourChanger.ini

# TODO: set up nginx config