from flask import Flask, request
from urlparse import parse_qs
import random
import urllib, urllib2
import redis, json
from datetime import datetime
application = Flask(__name__)


#function to change the colour saved in currentColour.txt
def changeColour(colour):
	if isinstance(colour, basestring):
		#access the redis database
		redis_db = redis.Redis(host = 'localhost', db = 0)
		#add the current time and new colour value as a json
		redis_db.rpush('entries','{"time":"' + str(datetime.now()) + '", "colour-to":"' + colour + '"}')

#function to request the colour saved in currentColour.txt
def requestColour():
	#access the redis database
	redis_db = redis.Redis(host = 'localhost', db = 0)
	colour = json.loads(redis_db.lindex('entries', -1))["colour-to"]
	return colour

#/ will be the location of the webapp
@application.route("/", methods = ['GET','POST'])
def hello():
	if request.method == 'POST':
		request_data = parse_qs(request.get_data())
		print request_data
		if request_data['action'][0] == 'update':
			pass
			#first, check the server for the colour
			colour = requestColour()
			#then, if the local colour is the same, do nothing
			#TODO: this will only make sense when each user has a static colour
			#otherwise, update the server
			changeColour("#%06x" % random.randint(0, 0xFFFFFF))
	print "Someone just accessed /."
	#determine the currentColour on initial access of the page
	colour = requestColour()
	return "\
		<body style='background-color:" + colour + ";'>\
			<form action='' method='POST'>\
				<button name ='action' value='update' style='display:block; width:100%; height:100%; background:" + colour + "; border:0;'></button>\
			</form>\
		</body>"

#if a post request is received:
@application.route("/app", methods = ['POST'])
def changeColourPost():
	if request.method == "POST":
		print "post request received."
		request_data = parse_qs(request.get_data())
		print "data parsed."
		if request_data['type'][0] == "change":
			print "change request received"
			changeColour(request_data['colour'][0])
			return "Colour has been changed."
		elif request_data['type'][0] == "request":
			print "request request received"
			return requestColour()
		else:
			return "Unrecognised request type."
	else:
		return "Not a POST request"

if __name__ == "__main__":
    application.run()
