# stdlib
import logging
import json
from random import randint

# 3rd party
from flask import \
    Blueprint,\
    request,\
    render_template

 # local
from database import Database

logger = logging.getLogger(__name__)

routes = Blueprint('play_routes', __name__, template_folder='templates')

moves = []
users_score = 0


@routes.route("/play")
def simon_says():
	logger.info('/')
	return render_template('simon_says.html')

@routes.route("/get-move", methods=['POST', 'GET'])
def get_move():
	global users_score
	logger.info('/get-move')
	data = json.loads(request.data)
	moves = data.get('moves')
	new_game = data.get('new')

	if new_game:
		users_score = 0

	moves.append(randint(1, 4))
	return json.dumps({'moves': moves, 'user': users_score})

@routes.route("/check-move", methods=['POST'])
def check_move():
	global users_score
	logger.info('/check-move')
	data = json.loads(request.data)
	simons_moves = data.get('simons_moves')
	users_moves = data.get('moves')
	timeout = data.get('timeout')
	len_users_moves = len(users_moves)
	len_simons_moves = len(simons_moves)

	if len_users_moves == 0:
		return json.dumps({'valid': False, 'user': users_score})

	if timeout and len_users_moves < len_simons_moves:
		return json.dumps({'valid': False, 'user': users_score})

	# This shouldn't ever happen, but just to be safe
	if len_users_moves > len_simons_moves:
		return json.dumps({'valid': False, 'user': users_score})

	simons_moves = simons_moves[:len_users_moves]
	if simons_moves == users_moves:
		users_score += 1
		return json.dumps({'valid': True, 'user': users_score})
	return json.dumps({'valid': False, 'user': users_score})