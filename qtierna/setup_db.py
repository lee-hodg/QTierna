import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from contextlib import contextmanager

from qtierna_settings import APP_DATA_PATH

db_path = os.path.join(APP_DATA_PATH, "reminders.db")
engine = create_engine('sqlite:///%s' % db_path, echo=False)
# Scoped session for thread safety, c.f.
# http://docs.sqlalchemy.org/en/latest/orm/contextual.html#contextual-thread-local-sessions
# Notice this provides the same session in given thread, but not accross multi threads
# Kind of like a global session so we don't have to pass around an object
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# Should not be opening a single eternal session per thread, but rather around
# each unit of work see
# http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_create_tables():
    # from models import Reminder, Category
    from models import Base
    # Create the database tables if they don't exist
    Base.metadata.create_all(engine)


def db_drop_all_tables():
    # from models import Reminder, Category
    from models import Base
    # Create the database tables if they don't exist
    Base.metadata.drop_all(engine)
