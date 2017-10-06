# stdlib
import datetime
import os 

# 3rd party 
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

# local
from database import db
from routes.play import routes as play_routes # noqa
from routes.index import routes as index_routes # noqa


def create_app():
	app = Flask(__name__)
	app.debug = True

	# Point application to psql database, initialize 
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app) 
	
	# Register the route files
	app.register_blueprint(play_routes)
	app.register_blueprint(index_routes)
	
	# Set secret key for session, set a lifetime on the session
	app.secret_key = os.environ['APP_SECRET_KEY']
	app.permanent_session_lifetime = datetime.timedelta(hours=8)
	return app


if __name__ == "__main__":
	app = create_app()
	app.run()
