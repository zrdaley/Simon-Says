# stdlib
from flask import current_app
from random import randint

# 3rd party
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm.attributes import flag_modified

db = SQLAlchemy()


class Players(db.Model):
    user_id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(50))
    high_score = db.Column(db.Integer)

    def __init__(self, uid, un, hs):
        self.user_id = uid,
        self.username = un
        self.high_score = hs


class Database(object):

    def create_new_user(self, username, user_id):
        user = Players(user_id, username, None)
        db.session.add(user)
        db.session.commit()

    def get_high_score(self, user_id):
        user = Players.query.filter_by(user_id=user_id).first()
        return user.high_score

    def get_top_users(self):
        top_users = Players.query.filter(Players.high_score != None).order_by(Players.high_score).limit(3)
        return top_users

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

    def update_high_score(self, user_id, score):
        user = Players.query.filter_by(user_id=user_id).first()
        if user.high_score is None or score > user.high_score:
            user.high_score = score
            db.session.commit()
            return user.high_score
        return None

    def username_exists(self, username):
        user = Players.query.filter_by(username=username).first()
        if user:
            return True
        return False
