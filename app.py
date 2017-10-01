

from flask import Flask
 
 
app = Flask(__name__)
app.debug = True

from routes.play import routes as play_routes # noqa

app.register_blueprint(play_routes)
 
if __name__ == "__main__":
	app.run()

