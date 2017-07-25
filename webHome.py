from flask import Flask
application = Flask(__name__)


@application.route("/")
def hello():
    return "<h1 style='color:orange'>Hello There!</h1>"

if __name__ == "__main__":
    application.run()
