from flask import Flask, request
application = Flask(__name__)

#couple of simple URL request tests
#/ will be replaced with a page showing the current colour
@application.route("/")
def hello():
	print "Some guy or gal just accessed /."
	return "<center><div style='width:auto; padding:auto'><h1 style='color:purple'>Hello There!</h1></div></center>"

#example of another page
@application.route("/test")
def test():
	print "Some bloke just accessed /test."
	return "<h1 style='color:yellow'>Testing...</h1>"

#function to change the colour saved in currentColour.txt
def changeColour(colour):
	colourFile = open("currentColour.txt", "w")
	if isinstance(colour, basestring):
		colourFile.write(colour)
	colourFile.close()

#if a post request is received:
@application.route("/", methods = ['POST'])
def changeColourPost():
	if request.method == 'POST':
		print "post request received"
		print request.get_data()
		changeColour('fffeef')
		return "Colour has been changed."
	else:
		return "Colour has not been changed."


if __name__ == "__main__":
    application.run()
