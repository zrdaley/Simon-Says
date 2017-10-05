# stdlib
from flask import current_app
from random import randint

# 3rd party
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm.attributes import flag_modified

db = SQLAlchemy()


class Players(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    high_score = db.Column(db.Integer)
    current_score = db.Column(db.Integer)
    moves = db.Column(JSON)


    def __init__(self, uid, un, hs, cs, m):
        self.user_id = uid,
        self.username = un
        self.high_score = hs
        self.current_score = cs
        self.moves = m


class Database(object):

    def add_move(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        user.moves.append(randint(1, 4))
        moves = user.moves
        flag_modified(user, "moves")
        db.session.commit()
        return moves

    def create_new_user(self, username, user_id):
        user = Players(user_id, username, None, 0, [])
        db.session.add(user)
        db.session.commit()

    def get_score(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        return user.current_score

    def get_high_score(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        return user.high_score

    def get_username(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        if user:
            return user.username
        return None

    def get_user_id(self, username):
        user = Players.query.filter_by(username=username).first()
        if user:
            return user.user_id
        return None

    def increment_score(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        user.current_score += 1
        score = user.current_score
        db.session.commit()
        return score
    
    def reset_moves(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        user.moves = []
        flag_modified(user, "moves")
        db.session.commit()

    def set_score(self, user_id, value):
        user = Players.query.filter_by(user_id=user_id).first()
        user.current_score = value
        db.session.commit()

    def update_high_score(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        if user.high_score is None or user.current_score > user.high_score:
            user.high_score = user.current_score
            db.session.commit()
            return user.high_score
        return None

    def user_exists(self, username):
        user = Players.query.filter_by(username=username).first()
        if user:
            return True
        return False
