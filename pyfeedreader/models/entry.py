from pyfeedreader.models.ReadEntries import ReadEntry

__author__ = 'sis13'

from pyfeedreader.database import Model, db_session
from sqlalchemy import Column, Integer, String, Text


class Entry(Model):
    __tablename__ = "entry"
    id = Column('id', Integer, primary_key=True)
    feed_id = Column(Integer)
    published = Column(Integer)
    updated = Column(Integer)
    title = Column(String(1024))
    content = Column(Text)
    description = Column(String(256))
    link = Column(String(1024))
    remote_id = Column(String(1024))

    def __init__(self, feed_id=None, published=None, updated=None, title=None, content=None, description=None,
                 link=None, remote_id=None, unread=True):
        self.feed_id = feed_id
        self.published = published
        self.updated = updated
        self.title = title
        self.content = content
        self.description = description
        self.link = link
        self.remote_id = remote_id
        self.unread = unread

    @staticmethod
    def json_entry(entry, db_session, user_id):
        """
        Turns the entry object into a JSON ready dict object.

        :param entry: The entry you want to make JSON ready.

        :return: The JSON ready dict.
        """

        read_entry = db_session.query(ReadEntry).filter(ReadEntry.entry_id == entry.id,
                                                        ReadEntry.user_id == user_id).first()
        unread = read_entry is None

        return {
            "entry_id": entry.id,
            "feed_id": entry.feed_id,
            "published": entry.published,
            "updated": entry.updated,
            "title": entry.title,
            "content": entry.content,
            "description": entry.description,
            "link": entry.link,
            "remote_id": entry.remote_id,
            "unread": unread,
        }

    @staticmethod
    def json_list(entries, db_session, user_id):
        """
        Turns a list of entries into JSON ready entries.

        :param entries: The list of entries you want to turn into JSON ready dicts.

        :return: List of JSON ready dicts.
        """

        json_ready = []
        for entry in entries:
            json_ready.append(
                Entry.json_entry(entry, db_session, user_id)
            )

        return json_ready