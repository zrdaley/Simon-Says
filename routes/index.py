# stdlib
import uuid

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


@routes.route("/")
def index():
	return render_template('index.html')

@routes.route("/create_account")
def create():
	username = request.args.get('username')

	# Filter username
	if not username:
		return render_template('index.html', create_error="Please enter a valid username")
	if len(username) > MAX_USER_LENGTH:
		return render_template('index.html', create_error="Username cannot exceed 100 characters")
	if not username.isalnum():
		return render_template('index.html', create_error="Usernames can only contain a-z, A-Z, or 0-9")

	# Check if username exists
	if db.username_exists(username):
		return render_template('index.html', create_error="The username '{}' is already taken".format(username))
	
	# Create user ID, add user to db, set cookie for gameplay, redirect to game
	user_id = uuid.uuid4().hex
	session['user_id'] = user_id 
	db.create_new_user(username, str(user_id))
	return redirect(url_for('play_routes.simon_says'))

@routes.route("/login")
def login():
	username = request.args.get('username')

	# Filter username
	if not username:
		return render_template('index.html', login_error="Please enter a valid username")
	if len(username) > MAX_USER_LENGTH:
		return render_template('index.html', login_error="Username cannot exceed 100 characters")
	if not username.isalnum():
		return render_template('index.html', login_error="Usernames can only contain a-z, A-Z, or 0-9")

	# Check if username exists
	if not db.username_exists(username):
		return render_template('index.html', login_error="The username '{}' does not exist".format(username))
	
	# Set cookie for gameplay, redirect to game
	user_id = db.get_user_id(username)
	session['user_id'] = user_id 
	return redirect(url_for('play_routes.simon_says'))

@routes.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index_routes.index'))
	
