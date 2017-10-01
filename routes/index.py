# stdlib
import logging

# 3rd party
from flask import \
    Blueprint,\
    request,\
    render_template

 # local
from database import Database

logger = logging.getLogger(__name__)

routes = Blueprint('index_routes', __name__, template_folder='templates')

@routes.route("/")
def index():
	logger.info('/')
	return render_template('index.html')

@routes.route("/create_account")
def create():
	logger.info('/')
	return render_template('index.html')

@routes.route("/login")
def login():
	logger.info('/')
	return render_template('index.html')