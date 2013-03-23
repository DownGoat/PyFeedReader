__author__ = 'sis13'

from config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(config.get("db_connector"), convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
fs_engine = create_engine(config.get("db_connector"), convert_unicode=True)

fs_db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=fs_engine))

Model = declarative_base()
Model.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from pyfeedreader.models.user import User
    from pyfeedreader.models.directory import Directory
    from pyfeedreader.models.direntries import DirEntry
    from pyfeedreader.models.userfeeds import UserFeeds
    from pyfeedreader.models.ReadEntries import ReadEntry

    Model.metadata.create_all(bind=engine)