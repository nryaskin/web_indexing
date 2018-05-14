from sqlalchemy import Table, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from base import Base

link_words_assosiation = Table(
    'links_words', Base.metadata,
    Column('link', String(255), ForeignKey('links.link'), primary_key=True),
    Column('word', String(255), ForeignKey('words.word'), primary_key=True)
)

class Link(Base):
    __tablename__='links'

    link = Column(String(255), primary_key=True)
    date = Column(DateTime)
    words = relationship("Word", secondary=link_words_assosiation)

    def __repr__(self):
        return "Link(%s)" % (self.link)

    def __eq__(self, other):
        if isinstance(other, Link):
            return self.link == other.link
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    def __init__(self, link):
        self.link = link