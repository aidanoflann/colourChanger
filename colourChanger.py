from flask import Flask, request
from urlparse import parse_qs
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

#couple of simple URL request tests
#/ will be replaced with a page showing the current colour
@application.route("/")
def hello():
	print "Some guy or gal just accessed /."
	#determine the currentColour
	colour = requestColour()
	return "<center><div style='background-colour:" + colour + "width:auto; padding:auto'><h1 style='color:" + colour + "'>Hello There!</h1></div></center>"

#example of another page
@application.route("/test")
def test():
	print "Some bloke just accessed /test."
	return "<h1 style='color:yellow'>Testing...</h1>"

#if a post request is received:
@application.route("/", methods = ['POST'])
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
