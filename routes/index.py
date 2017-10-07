# stdlib
import uuid
import re

# 3rd party
from flask import \
    Blueprint,\
    current_app, \
    request,\
    redirect, \
    render_template, \
    session, \
    url_for

 # local
from database import Database

routes = Blueprint('index_routes', __name__, template_folder='templates')
db = Database()
MAX_USER_LENGTH = 50
PASSWORD_RE = '[A-Za-z0-9@#$%^&+=]{6,100}'


@routes.route("/")
def index():
	login_error = request.args.get('login_error')
	create_error = request.args.get('create_error')
	if login_error:
		return render_template('index.html', login_error=login_error)
	if create_error:
		return render_template('index.html', create_error=create_error)
	return render_template('index.html')

@routes.route("/create_account")
def create():
	username = request.args.get('username')
	password = request.args.get('password')

	# Filter username
	if not username:
		return redirect(url_for('index_routes.index', create_error="Please enter a valid username"))
	if len(username) > MAX_USER_LENGTH:
		return redirect(url_for('index_routes.index', create_error="Username cannot exceed 50 characters"))
	if not username.isalnum():
		return redirect(url_for('index_routes.index', create_error="Usernames can only contain a-z, A-Z, or 0-9"))
	# Check if username exists
	if db.account_exists(username):
		return redirect(url_for('index_routes.index', create_error="The username '{}' is already taken".format(username)))

	# Filter password
	if not re.match(PASSWORD_RE, password):
		return redirect(url_for('index_routes.index', create_error="Invalid password"))
	
	# Create user ID, add user to db, set cookie for gameplay, redirect to game
	user_id = uuid.uuid4().hex
	session['user_id'] = user_id 
	db.create_new_user(username, str(user_id), password)
	return redirect(url_for('play_routes.simon_says'))

@routes.route("/login")
def login():
	username = request.args.get('username')
	password = request.args.get('password')

	# Filter username
	if not username:
		return redirect(url_for('index_routes.index', login_error="Please enter a valid username"))
	if len(username) > MAX_USER_LENGTH:
		return redirect(url_for('index_routes.index', login_error="Username cannot exceed 50 characters"))
	if not username.isalnum():
		return redirect(url_for('index_routes.index', login_error="Usernames can only contain a-z, A-Z, or 0-9"))

	# Check if username exists
	if not db.account_exists(username):
		return redirect(url_for('index_routes.index', login_error="The username '{}' does not exist".format(username)))

	# Filter password
	if not re.match(PASSWORD_RE, password):
		return redirect(url_for('index_routes.index', login_error="Invalid password"))

	# Authenticate
	user_id = db.authenticate_user(username, password)
	if not user_id:
		return redirect(url_for('index_routes.index', login_error="Invalid credentials"))
	
	# Set cookie for gameplay, redirect to game
	session['user_id'] = user_id 
	return redirect(url_for('play_routes.simon_says'))

@routes.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index_routes.index'))
	
