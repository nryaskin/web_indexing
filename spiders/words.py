import itertools
from dao.base import Session
from dao.link import Link
from dao.word import Word

def words_by_url(url):
    session = Session()
    result = session.query(Link).filter(Link.link.ilike('%' + url + '%')).all()
    if result:
        return [w.word for w in set(itertools.chain.from_iterable(l.words for l in result))]
    return []