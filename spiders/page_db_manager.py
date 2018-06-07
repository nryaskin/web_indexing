# coding=utf-8
import datetime
import re
import sys
import requests
from lxml import html
from dao.base import Session, engine, Base
from dao.link import Link
from dao.word import Word


class Spider:



    def __init__(self):
        self.session = Session()
        self.dead_links = set()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.commit()
        self.session.close()

    def get_links(self, base_link, htmlElement):
        links = set()
        if not base_link.link.startswith("http") :
            htmlElement.make_links_absolute(base_link.link, resolve_base_href=True)

        for elem in htmlElement.iterlinks():
            link = elem[2]  # get the link from elemnt which is at index 2
            links.add(Link(link))
        return links

    def get_words_set(self, text):
        occurence = set()
        text_string = text.lower()
        match_pattern = re.findall(r'\b[a-zа-я]{3,15}\b', text_string)
        for word in match_pattern:
            occurence.add(Word(word))
        return occurence

    def parse_page(self, base_link):
        response = requests.get(base_link.link)
        sourceCode = response.content
        links = set()
        if len(sourceCode) > 0 :
            htmlElement = html.document_fromstring(sourceCode)
            text = htmlElement.text_content()
            base_link.words = list(self.get_words_set(text))
            base_link.date = datetime.datetime.now()
            #TODO: write to database
            #session = Session()
            self.session.merge(base_link)
            #self.session.commit()
            #session.close()
            links = self.get_links(base_link, htmlElement)
        else :
            self.dead_links.add(base_link)
        return links

    def valid_for_domain(self, domain, exclude_arr):
        def is_valid_link(link):
            link_addr = link.link
            file_extension = link_addr.split(".")[-1]
            regex = r"^https?://" + domain
            if (file_extension not in exclude_arr) and (re.match(regex, link_addr) is not None):
                return True
            return False
        return is_valid_link


    def walk_links(self, base_link, is_valid_link):
        links = self.parse_page(base_link)
        page_links = set(filter(is_valid_link, links))
        links_c = list(self.session.query(Link).filter(Link.link.in_(map(lambda x : x.link, page_links))))
        links = map(lambda x: x.link, links_c)
        page_new_links = filter(lambda x: x.link not in links, page_links)
        page_new_links = set(page_new_links).difference(self.dead_links)
        for link in page_new_links:
            self.session.merge(link)
        self.session.commit()
        print 'Found %s new links at %s' % (len(page_new_links), base_link)
        for new_link in page_new_links:
            self.walk_links(new_link, is_valid_link)


if __name__ == '__main__':
    #Base.metadata.create_all(engine)
    print "Start link collecting"
    #"https://www.cs.vsu.ru"
    arr = set(["css", "js", "ico", "jpg", "png"])
    domain = "www.cs.vsu.ru"
    with Spider() as spider:
        is_valid_link = spider.valid_for_domain(domain, arr)
        base_link = Link("https://www.cs.vsu.ru")
        try:
            spider.walk_links(base_link, is_valid_link)
        except requests.exceptions.ConnectionError as e:
            print e
            sys.exit(1)
        print "End of link collecting"
        print "--end--"
