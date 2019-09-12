from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class TagQuery(Base):
    """Tagquery table model"""

    __tablename__ = 'TagQuery'
    id = Column(Integer, primary_key=True)
    site_name = Column(String(250), nullable=False)
    full_url = Column(String(250), nullable=False)
    query_date = Column(DateTime(timezone=False), nullable=False, default=datetime.datetime.now())
    tag_data = Column(LargeBinary, nullable=False)
