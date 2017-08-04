from flask import Flask, request, session, url_for, redirect
from urlparse import parse_qs
import random
import redis
import json
import hashlib
from dateutil import parser
from datetime import datetime
application = Flask(__name__)

# generate a redis_db variable
redis_db = redis.Redis(host="redis-10949.c2.eu-west-1-3.ec2.cloud.redislabs.com", port="10949")
# redis_db = redis.Redis()
# if you're not Aidan O'Flannagain don't read the next line
application.secret_key = '\x94\xe5\xac\xed\x00*A\x9f\xf1\x98\x91\xcd\x94\xba\x8b\x8e\xf5>\xe4\x98\xa0\xcc\xba\x9b'


@application.before_request
def before_request():
    """
    open redis connection before requests
    """
    redis_db = redis.Redis(host='localhost', db=0)


@application.teardown_request
def teardown_request(exeption):
    """
    close redis connection after request construction
    :param exeption: 
    :return: 
    """
    redis_db.connection_pool.disconnect()


def change_colour(colour):
    """
    change the colour saved in redis database
    :param colour: 
    :return: 
    """
    if colour == request_colour():
        # no need to write to the db, the colour is already set
        return
    if isinstance(colour, basestring):
        # add the current time and new colour value as a json
        redis_db.rpush('entries', '{"time":"' + str(datetime.utcnow()) + '", "colour-to":"' + colour + '"}')


def request_colour():
    """
    request the colour saved in redis database
    :return: 
    """
    stored_colour = redis_db.lindex('entries', -1)
    if stored_colour is None:
        return "#000000"
    colour = json.loads(stored_colour)["colour-to"]
    return colour


def get_last_change_time():
    """ Get a string representing the last time the colour was changed.
    
    :return: 
    """
    stored_time = redis_db.lindex('entries', -1)
    if stored_time is None:
        return None
    time = json.loads(stored_time)["time"]
    return time


# / will be the location of the webapp
@application.route("/", methods=['GET', 'POST'])
def root_page():
    if session.get('logged_in'):
        # temporarily redirecting to login in all cases while session issue is resolved
        return redirect('/login')
        if request.method == 'POST':
            request_data = parse_qs(request.get_data())
            print request_data
            if request_data['action'][0] == 'update':
                #first, check the server for the colour
                colour = request_colour()
                #then, if the local colour is not the same, change the colour
                if not redis_db.hmget('user:'+session['username'],'colour') == colour:
                    change_colour(redis_db.hmget('user:' + session['username'], 'colour'))
        print "Someone just accessed /."
        
        # determine the currentColour on initial access of the page
        colour = request_colour()
        return "\
            <body style='background-color:" + colour + ";'>\
                <form action='' method='POST'>\
                    <button name ='action' value='update' style='display:block; width:100%; height:100%; background:" + colour + "; border:0;'></button>\
                </form>\
            </body>"
    else:
        return redirect(url_for("login"))


@application.route("/login", methods=['GET', 'POST'])
def login():
    colour = request_colour()
    last_change_time = parser.parse(get_last_change_time())
    days, hours, minutes, seconds = days_hours_minutes_seconds(datetime.utcnow(), last_change_time)
    if request.method == "GET":
        return "<body style = 'background-color:" + colour + "'>\
            <center><div style = 'background-color:white; color:black; width:40%;'><br>\
                Please enter your username and password below.<br>\
                If you don't have an account, one will be created.<br>\
                <form method='POST'>\
                    username: <input type='text' name='username'><br>\
                    password: <input type='password' name='password'><br><br>\
                    <input type='submit',  value='Login'>\
                </form><br>\
                This page has been <span style='color:{}'>{}</span> for <br>\
                {} days, {} hrs, {} mins, and {} secs.<br>\
            <br>\
            </center></div>\
            </body>".format(colour, colour, days, hours, minutes, seconds)
    elif request.method == "POST":
        request_data = parse_qs(request.get_data())
        # first, redirect if either the username or pass were empty
        if not ('username' in request_data.keys() and 'password' in request_data.keys()):
            return redirect('/login')
        pass_hashed = hashlib.md5(request_data['password'][0]).digest()
        session['logged_in'] = True
        session['username'] = request_data['username'][0]
        # if the user doesn't exist already...
        if not 'user:'+session['username'] in redis_db.keys():
            # add his username and pass, and assign him a random colour
            redis_db.hmset('user:'+session['username'],{'password':pass_hashed, 'colour': '#%06x' % random.randint(0, 0xFFFFFF)})
            change_colour(redis_db.hmget('user:' + session['username'], 'colour')[0])
            return redirect('/')
        # if it does, compare passwords
        else:
            if pass_hashed == redis_db.hmget('user:'+session['username'],'password')[0]:
                change_colour(redis_db.hmget('user:' + session['username'], 'colour')[0])
                return redirect('/login')
            else:
                return redirect('/login')
        

# if a post request is received:
@application.route("/app", methods = ['POST'])
def change_colour_post():
    if request.method == "POST":
        print "post request received."
        request_data = parse_qs(request.get_data())
        print "data parsed."
        if request_data['type'][0] == "change":
            print "change request received"
            change_colour(request_data['colour'][0])
            return "Colour has been changed."
        elif request_data['type'][0] == "request":
            print "request request received"
            return request_colour()
        else:
            return "Unrecognised request type."
    else:
        return "Not a POST request"


def days_hours_minutes_seconds(new_time, old_time):
    "Return tuple"
    td = new_time - old_time
    return td.days, td.seconds/3600, (td.seconds/60)%60, td.seconds%60

if __name__ == "__main__":
    application.run()
