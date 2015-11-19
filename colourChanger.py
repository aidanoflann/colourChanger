from flask import Flask, request, session, url_for, redirect, flash
from urlparse import parse_qs
import random
import urllib, urllib2
import redis, json
import hashlib
from datetime import datetime
application = Flask(__name__)

#generate a redis_db variable
redis_db = redis.Redis()
#if you're not Aidan O'Flannagain don't read the next line
application.secret_key = '\x94\xe5\xac\xed\x00*A\x9f\xf1\x98\x91\xcd\x94\xba\x8b\x8e\xf5>\xe4\x98\xa0\xcc\xba\x9b'

#open redis connection before requests
@application.before_request
def before_request():
	redis_db = redis.Redis(host = 'localhost', db = 0)

#close redis connection after request construction
@application.teardown_request
def teardown_request(exeption):
	redis_db.connection_pool.disconnect()

#function to change the colour saved in redis database
def changeColour(colour):
	if isinstance(colour, basestring):
		#add the current time and new colour value as a json
		redis_db.rpush('entries','{"time":"' + str(datetime.now()) + '", "colour-to":"' + colour + '"}')

#function to request the colour saved in redis database
def requestColour():
	colour = json.loads(redis_db.lindex('entries', -1))["colour-to"]
	return colour

#/ will be the location of the webapp
@application.route("/", methods = ['GET','POST'])
def rootPage():
	if session.get('logged_in'):
		#temporarily redirecting to login in all cases while session issue is resolved
		return redirect('/login')
		if request.method == 'POST':
			request_data = parse_qs(request.get_data())
			print request_data
			if request_data['action'][0] == 'update':
				#first, check the server for the colour
				colour = requestColour()
				#then, if the local colour is not the same, change the colour
				if not redis_db.hmget('user:'+session['username'],'colour') == colour:
					changeColour(redis_db.hmget('user:'+session['username'],'colour'))
		print "Someone just accessed /."
		#determine the currentColour on initial access of the page
		colour = requestColour()
		return "\
			<body style='background-color:" + colour + ";'>\
				<form action='' method='POST'>\
					<button name ='action' value='update' style='display:block; width:100%; height:100%; background:" + colour + "; border:0;'></button>\
				</form>\
			</body>"
	else:
		return redirect(url_for("login"))

@application.route("/login", methods = ['GET','POST'])
def login():
	colour = requestColour()
	if request.method == "GET":
		return "<body style = 'background-color:" + colour + "'>\
			<center><div style = 'background-color:white; color:black; width:40%;'>\
				Please enter your username and password below.<br>\
				If you don't have an account, one will be created.<br>\
				<form method='POST'>\
					username: <input type='text' name='username'><br>\
					password: <input type='password' name='password'><br>\
					<input type='submit'>\
				</form>\
			</center></div>\
			</body>"
	elif request.method == "POST":
		request_data = parse_qs(request.get_data())
		#first, redirect if either the username or pass were empty
		if not ('username' in request_data.keys() and 'password' in request_data.keys()):
			return redirect('/login')
		pass_hashed = hashlib.md5(request_data['password'][0]).digest()
		session['logged_in'] = True
		session['username'] = request_data['username'][0]
		#if the user doesn't exist already...
		if not 'user:'+session['username'] in redis_db.keys():
			#add his username and pass, and assign him a random colour
			redis_db.hmset('user:'+session['username'],{'password':pass_hashed, 'colour': '#%06x' % random.randint(0, 0xFFFFFF)})
			changeColour(redis_db.hmget('user:'+session['username'],'colour')[0])
			return redirect('/')
		#if it does, compare passwords
		else:
			if pass_hashed == redis_db.hmget('user:'+session['username'],'password')[0]:
				changeColour(redis_db.hmget('user:'+session['username'],'colour')[0])
				return redirect('/login')
			else:
				return redirect('/login')
		

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

#if __name__ == "__main__":
