import os 
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from database import db
from routes.play import routes as play_routes # noqa


def create_app():
	app = Flask(__name__)
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app) 
	app.register_blueprint(play_routes)
	return app


if __name__ == "__main__":
	app = create_app()
	app.run()

