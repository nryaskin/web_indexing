import itertools
from dao.base import Session
from dao.word import Word


def urls_by_word(word):
    session = Session()
    result = session.query(Word).filter(Word.word.ilike('%' + word + '%')).all()
    if result:
        return [link.link for link in set(itertools.chain.from_iterable(w.links for w in result))]
    return []