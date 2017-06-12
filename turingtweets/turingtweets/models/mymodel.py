from sqlalchemy import (
    Column,
    Unicode,
    Integer,
)

from .meta import Base


class Tweet(Base):
    """Model for a single tweet."""

    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tweet = Column(Unicode)
