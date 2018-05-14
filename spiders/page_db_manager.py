# coding=utf-8
import requests
import re
import sys
from lxml import html

import datetime

from dao.base import Session, engine, Base
from dao.link import Link
from dao.word import Word


def get_links(base_link, htmlElement):
    links = set()
    htmlElement.make_links_absolute(base_link.link, resolve_base_href=True)

    for elem in htmlElement.iterlinks():
        link = elem[2]  # get the link from elemnt which is at index 2
        links.add(Link(link))
    return links

def get_words_set(text):
    occurence = set()
    text_string = text.lower()
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
    for word in match_pattern:
        occurence.add(Word(word))
    return occurence

def parse_page(base_link):
    response = requests.get(base_link.link)
    sourceCode = response.content

    htmlElement = html.document_fromstring(sourceCode)
    text = htmlElement.text_content()
    base_link.words = list(get_words_set(text))
    base_link.date = datetime.datetime.now()
    #TODO: write to database
    session = Session()
    session.merge(base_link)
    session.commit()
    session.close()
    return get_links(base_link, htmlElement)

def valid_for_domain(domain, exclude_arr):
    def is_valid_link(link):
        link_addr = link.link
        file_extension = link_addr.split(".")[-1]
        regex = r"^https?://" + domain
        if (file_extension not in exclude_arr) and (re.match(regex, link_addr) is not None):
            return True
        return False
    return is_valid_link


def walk_links(base_link, is_valid_link):
    links = parse_page(base_link)
    page_links = set(filter(is_valid_link, links))
    #TODO: query  links that are already in database
    session = Session()
    links_c = session.query(Link).filter(Link.link.in_(map(lambda x : x.link, page_links)))
    links = map(lambda x: x.link, links_c)
    page_new_links = filter(lambda x: x.link not in links, page_links)
    #TODO: save links to database
    session.add_all(page_new_links)
    #valid_links |= page_new_links
    session.commit()
    session.close()
    for new_link in page_new_links:
        walk_links(new_link, is_valid_link)



print "Start link collecting"
#"https://www.cs.vsu.ru"
arr = set(["css", "js", "ico", "jpg", "png"])
domain = "www.python.org"
is_valid_link = valid_for_domain(domain, arr)

base_link = Link("https://www.python.org")


try:
    walk_links(base_link, is_valid_link)
except requests.exceptions.ConnectionError as e:
    print e
    sys.exit(1)
print "End of link collecting"
print "--end--"

#print text

