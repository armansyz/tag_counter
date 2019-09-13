from db_model import TagQuery
from db_connection import SessionManager, engine
from sqlite3 import OperationalError
from loguru import logger


class TagManager(SessionManager):
    """Class contains methods for managing interaction with the database"""

    @staticmethod
    def create_tables():
        """Creates TagQuery table by checking if it exists first"""
        try:
            TagQuery.__table__.create(bind=engine, checkfirst=True)
        except OperationalError as oe:
            logger.error('Table already exists \n Exception:{}'.format(oe))

    def insert_tag(self, site_name, full_url, tag_data):
        """Inserts TagQuery record into the database"""
        try:
            self.session.add(TagQuery(site_name=site_name, full_url=full_url, tag_data=tag_data))
            self.session.commit()
        except OperationalError as oe:
            logger.error('Failed to insert new record \n Exception:{}'.format(oe))

    def get_tag(self, full_url) -> TagQuery:
        """Attempts to retrieve the TagQuery object from the database"""
        try:
            return self.session.query(TagQuery).filter(TagQuery.full_url == full_url)
        except OperationalError as oe:
            logger.error('The table does not exist \n Exception:{}'.format(oe))
