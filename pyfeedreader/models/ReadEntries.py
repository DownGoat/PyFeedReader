__author__ = 'sis13'

from sqlalchemy import Column, Integer, ForeignKey

from pyfeedreader.database import Model


class ReadEntry(Model):
    __tablename__ = "ReadEntry"
    id = Column('id', Integer, primary_key=True)
    entry_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, entry_id, user_id):
        self.entry_id = entry_id
        self.user_id = user_id

    def __repr__(self):
        return '<ReadEntry %r>' % self.username