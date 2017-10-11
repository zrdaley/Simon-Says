# stdlib
import os
import hashlib

# 3rd party
from flask import current_app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Accounts(db.Model):
    user_id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    high_score = db.Column(db.Integer)

    def __init__(self, uid, un, pw, hs):
        self.user_id = uid,
        self.username = un
        self.password = pw
        self.high_score = hs


class Database(object):

    def _hash_password(self, password):
        # Salt and hash password for storage
        h = hashlib.md5((password + os.environ['SALT']).encode('utf-8'))
        password_hash = h.hexdigest()
        return password_hash

    def account_exists(self, username):
        account = Accounts.query.filter_by(username=username).first()
        if account:
            return True
        return False

    def authenticate_user(self, username, password):
        account = Accounts.query.filter_by(username=username).first()
        password_hash = self._hash_password(password)
        if password_hash == str(account.password):
            return account.user_id
        return None

    def create_new_user(self, username, user_id, password):
        account = Accounts(user_id, username, self._hash_password(password), None)
        db.session.add(account)
        db.session.commit()

    def get_high_score(self, user_id):
        user = Accounts.query.filter_by(user_id=user_id).first()
        return user.high_score

    def get_top_users(self):
        top_users = Accounts.query.filter(Accounts.high_score != None).order_by(Accounts.high_score).limit(3)
        return top_users

    def get_username(self, user_id):
        user = Accounts.query.filter_by(user_id=user_id).first()
        if user:
            return user.username
        return None

    def get_user_id(self, username):
        user = Accounts.query.filter_by(username=username).first()
        if user:
            return user.user_id
        return None

    def update_high_score(self, user_id, score):
        user = Accounts.query.filter_by(user_id=user_id).first()
        if user.high_score is None or score > user.high_score:
            user.high_score = score
            db.session.commit()
            return user.high_score
        return None
