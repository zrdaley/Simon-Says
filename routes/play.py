# stdlib
import json
from random import randint

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

db = Database()

routes = Blueprint('play_routes', __name__, template_folder='templates')


# Reset the session timeout while the user is playing
@routes.before_request
def before_request():
    session.permanent = True
    session.modified = True

@routes.route("/play")
def simon_says():
	user_id = session.get('user_id')

	# Check if the user has a valid session
	if not user_id:
		return redirect(url_for('index_routes.login'))

	# Check if the cookie is valid
	user = db.get_username(user_id)
	if not user:
		return redirect(url_for('index_routes.login'))

	return render_template('simon_says.html', user=user, high_score=db.get_high_score(user_id))

@routes.route("/get-move", methods=['POST', 'GET'])
def get_move():
	user_id = session.get('user_id')
	
	# Check if the user has a valid session
	if not user_id:
		return redirect(url_for('index_routes.login'))

	data = json.loads(request.data)
	moves = data.get('moves')
	new_game = data.get('new')

	# Check if the user has started a new game
	if new_game:
		session['score'] = 0
		session['moves'] = []

	# Get the users score, get a new move
	users_score = session.get('score')
	moves.append(randint(1, 4))
	session['moves'] = moves

	return json.dumps({'moves': moves, 'user': users_score})

@routes.route("/check-move", methods=['POST'])
def check_move():
	user_id = session.get('user_id')

	# Check if the user has a valid session
	if not user_id:
		return redirect(url_for('index_routes.login'))

	data = json.loads(request.data)
	simons_moves = data.get('simons_moves')
	users_moves = data.get('moves')
	timeout = data.get('timeout')
	
	len_users_moves = len(users_moves)
	len_simons_moves = len(simons_moves)

	users_score = session.get('score')

	def lose():
		new_hs = db.update_high_score(user_id, users_score)
		if new_hs is None:
			return json.dumps({'valid': False, 'user': users_score})
		return json.dumps({'valid': False, 'user': users_score, 'high_score': new_hs})
		
	# Check if the user has made a move
	if len_users_moves == 0:
		return lose()

	# Check if the user has run out of time
	if timeout and len_users_moves < len_simons_moves:
		return lose()

	# A user should never have more moves than simon, but JIC
	if len_users_moves > len_simons_moves:
		return lose()

	# Cast simons moves to the length of user moves and compare
	simons_moves = simons_moves[:len_users_moves]
	if simons_moves == users_moves:
		if len_simons_moves == len_users_moves:
			users_score += 1
			session['score'] = users_score
		return json.dumps({'valid': True, 'user': users_score})
	
	return lose()
