from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    Boolean,
)

from .meta import Base


class Tweet(Base):
    """Model for a single tweet."""

    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    tweet = Column(Unicode)


class FakeTweet(Base):
    """Model for a single fake tweet."""
    __tablename__ = 'fake-tweets'
    id = Column(Integer, primary_key=True)
    faketweet = Column(Unicode)
    tweeted = Column(Boolean)
    shown = Column(Integer)
    chosen = Column(Integer)
