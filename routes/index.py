# 3rd party
from flask import \
    Blueprint,\
    current_app, \
    request,\
    redirect, \
    render_template

 # local
from database import Database

routes = Blueprint('index_routes', __name__, template_folder='templates')
db = Database()

@routes.route("/")
def index():
	return render_template('index.html')

@routes.route("/create_account")
def create():
	username = request.args.get('username')

	# Filter username
	if not username:
		return render_template('index.html', create_error="Please enter a valid username")
	if not username.isalnum():
		return render_template('index.html', create_error="Usernames can only contain a-z, A-Z, or 0-9")

	# Check if username exists
	if db.user_exists(username):
		return render_template('index.html', create_error="The username '{}' is already taken".format(username))
	
	# Add username to db, set cookie for gameplay, redirect to game
	db.create_new_user(username)
	redirect_to_index = redirect('/play')
	response = current_app.make_response(redirect_to_index)
	response.set_cookie('simon-says-by-zen',value=username)
	return response

@routes.route("/login")
def login():
	username = request.args.get('username')
	if not username:
		return render_template('index.html', login_error="Please enter a valid username")
	if not username.isalnum():
		return render_template('index.html', login_error="Usernames can only contain a-z, A-Z, or 0-9")

	# Check if username exists
	if not db.user_exists(username):
		return render_template('index.html', create_error="The username '{}' does not exist".format(username))
	
	# Set cookie for gameplay, redirect to game
	redirect_to_index = redirect('/play')
	response = current_app.make_response(redirect_to_index)
	response.set_cookie('simon-says-by-zen',value=username)
	return response
	
	return render_template('index.html')