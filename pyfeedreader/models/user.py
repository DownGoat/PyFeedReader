__author__ = 'sis13'

from pyfeedreader.database import Model
from sqlalchemy import Column, Integer, String, Text


class User(Model):
    __tablename__ = "user"
    id = Column('id', Integer, primary_key=True)
    email = Column(String(256))
    password = Column(Text)
    salt = Column(String(20))
    current_login = Column(Integer)
    last_login = Column(Integer)
    username = Column(String(100))

    def __init__(self, email=None, password=None, salt=None, current_login=None,
                 last_login=None, username=None):
        self.email = email
        self.password = password
        self.salt = salt
        self.current_login = current_login
        self.last_login = last_login
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username