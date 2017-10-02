# stdlib
import json
from random import randint

# 3rd party
from flask import \
    Blueprint,\
    current_app, \
    request,\
    redirect, \
    render_template

 # local
from database import Database

db = Database()

routes = Blueprint('play_routes', __name__, template_folder='templates')


@routes.route("/play")
def simon_says():
	user = request.cookies.get('simon-says-by-zen')
	if not user:
		return redirect(url_for('index'))
	return render_template('simon_says.html', user=user, high_score=db.get_high_score(user))

@routes.route("/get-move", methods=['POST', 'GET'])
def get_move():
	user = request.cookies.get('simon-says-by-zen')
	data = json.loads(request.data)
	
	moves = data.get('moves')
	new_game = data.get('new')

	if new_game:
		current_app.logger.debug("RESTARTING")
		db.set_score(user, 0)
		db.reset_moves(user)

	users_score = db.get_score(user)
	moves = db.add_move(user)
	return json.dumps({'moves': moves, 'user': users_score})

@routes.route("/check-move", methods=['POST'])
def check_move():
	user = request.cookies.get('simon-says-by-zen')
	data = json.loads(request.data)
	
	simons_moves = data.get('simons_moves')
	users_moves = data.get('moves')

	current_app.logger.info("moves: {}".format(str(users_moves)))
	current_app.logger.info("sim_moves: {}".format(str(simons_moves)))
	
	timeout = data.get('timeout')
	
	len_users_moves = len(users_moves)
	len_simons_moves = len(simons_moves)

	users_score = db.get_score(user)

	# Check if the user has made a move
	if len_users_moves == 0:
		db.reset_moves(user)
		db.update_high_score(user)
		return json.dumps({'valid': False, 'user': users_score})

	# Check if the user has run out of time
	if timeout and len_users_moves < len_simons_moves:
		db.reset_moves(user)
		db.update_high_score(user)
		return json.dumps({'valid': False, 'user': users_score})

	# A user should never have more moves than simon, but JIC
	if len_users_moves > len_simons_moves:
		db.reset_moves(user)
		db.update_high_score(user)
		return json.dumps({'valid': False, 'user': users_score})

	# Cast simons moves to the length of user moves and compare
	simons_moves = simons_moves[:len_users_moves]
	if simons_moves == users_moves:
		if len_simons_moves == len_users_moves:
			users_score = db.increment_score(user)
			current_app.logger.info("INC")
		return json.dumps({'valid': True, 'user': users_score})
	db.reset_moves(user)
	db.update_high_score(user)
	return json.dumps({'valid': False, 'user': users_score})