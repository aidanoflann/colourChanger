from flask import Flask, request
from urlparse import parse_qs
import random
import urllib, urllib2
application = Flask(__name__)


#function to change the colour saved in currentColour.txt
def changeColour(colour):
	colourFile = open("currentColour.txt", "w")
	if isinstance(colour, basestring):
		colourFile.write(colour)
	colourFile.close()

#function to request the colour saved in currentColour.txt
def requestColour():
	colourFile = open("currentColour.txt", "r")
	colour = colourFile.read()
	colourFile.close()
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
