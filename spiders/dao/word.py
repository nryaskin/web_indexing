from sqlalchemy import Column, String, Integer

from base import Base

class Word(Base):
    __tablename__='words'

    word = Column(String(255), primary_key=True)

    def __repr__(self):
        return "Word(%s)" % (self.word)

    def __eq__(self, other):
        if isinstance(other, Word):
            return self.word == other.word
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    def __init__(self, word):
        self.word = word