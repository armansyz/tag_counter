from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger


try:
    engine = create_engine('sqlite:///database.db')
except Exception as e:
    logger.error('Failed to create engine \n Exception:{}'.format(e))

# create a Session
Session = sessionmaker(bind=engine)


class SessionManager(object):
    """A class to manage the session"""

    def __init__(self) -> object:
        self.session = Session()
