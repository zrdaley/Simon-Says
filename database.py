# stdlib
import logging

# 3rd party
from flask.ext.sqlalchemy import SQLAlchemy

# local
from config import CONFIG

db = SQLAlchemy()

logger = logging.getLogger(__name__)

class Players(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    high_score = db.Column(db.Integer)
    current_score = db.Column(db.Integer)

    def __init__(self, un, hs, cs):
        self.username = un
        self.high_score = hs
        self.current_score = cs


class Database(object):

    def create_new_user(self, username):
        user = Players(username, None, 0)
        db.session.add(user)
        db.session.commit()
