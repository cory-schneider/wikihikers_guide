#!/usr/bin/python3

# Why are citations left sometimes?: teratoma

from bs4 import BeautifulSoup
import requests
import re
from PIL import Image
import img_manip
from time import sleep
import sys
import pygame as pg
import urllib.request

testing = True

def remove_chars(text, regex):
        rgx = re.compile(regex)
        while rgx.search(text):
            chars_to_cut = rgx.search(text).group()
            text = text.replace(chars_to_cut, "")

        return text

def url_cleaning(muddy_url):
    url_regex = re.compile(r'https://en.wikipedia.org/wiki/[^&]*')
    clean_url = url_regex.search(muddy_url).group()
    regex = r'%[0-9]*'
    clean_url = remove_chars(clean_url, regex)

    return clean_url

def image_url_cleaning(muddy_url):
    url_regex = re.compile(r'upload.wikimedia.org/[^"]*')
    clean_url = url_regex.search(muddy_url).group()
    return clean_url

def request_soup(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def get_wiki_url(search_terms):
    """
    Requests source code for a Google search for the user's search terms and
    selects the first result. This helps clear up any errors and gets the user
    to a relevant wiki page.
    """
    url = 'https://www.google.com/search?q=site:https://en.wikipedia.org/+' + search_terms

    soup = request_soup(url)
    wiki_link = str(soup.find(href=re.compile(
        "https://en.wikipedia.org/wiki/[^&]*")))
    wiki_url = url_cleaning(wiki_link)

    return wiki_url

def remove_citations(p_text):
        citation_regex = r'\[[0-9]*\]'
        p_text = remove_chars(p_text, citation_regex)

        return p_text

def scrape_wiki(wiki_url):
    # Request document source and initialize soup for wikipedia article
    soup = request_soup(wiki_url)
    # ADD A TEST FOR FUNCTIONING WIKI ARTICLE!
    # Scrape the title from the Wiki
    title = soup.find("h1")
    title = title.text.strip()

    # Scraping a suitable image
    url_list = []
    img_url = "Macarena"
    jpg_urls = soup.find_all(src=re.compile(".jpg$"))
    if jpg_urls:
        for i in jpg_urls:
            new_jpg = image_url_cleaning(str(i))
            url_list.append(new_jpg)
    else:
        print("BYEEEEEEE")
        quit()

    # Scraping a summary
    summary = []
    element = soup.find("p")

    # Usually, the first <p> element is empty except for class "mw-empty-elt"
    # and it needs to be ignored. If not, we want to add it.
    if not element.has_attr("class"):
        summary.append(element.text)

    while element.name != "style" and len(summary) < 3:
        element = element.next_element
        if element.name == "p" and not element.find_parents("table"):
            summary_para = remove_citations(element.text)
            summary.append(summary_para)

    return title, summary, img_url

input = input("Don't Panic> ")
search_terms = input.replace(' ', '+')

wiki_url = get_wiki_url(search_terms)
print(f"Wikipedia URL: {wiki_url}")

title, summary, img_url = scrape_wiki(wiki_url)
print(f"Image location: {img_url}")

# path = img_manip.guide_ify(img_url)

# print(path)

# pg.init()
# screen = pg.display.set_mode((800, 800))
# pg.display.set_caption("Wikihiker's Guide")
# screen_rect = screen.get_rect()
# clock = pg.time.Clock()
#
# font = pg.font.Font(None, 48)
# rendered_text = font.render(title, True, pg.Color("dodgerblue"))
# text_rect = rendered_text.get_rect(midleft=(900, screen_rect.centery))
#
# image = pg.image.load(path)
#
# done = False
# while not done:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             done = True
#
#     if text_rect.centerx > screen_rect.centerx:
#         print(text_rect.centerx)
#         text_rect.move_ip(-5, 0)
#
#     screen.fill(pg.Color("gray5"))
#     screen.blit(rendered_text, text_rect)
#     screen.blit(image, (0, 0))
#
#
#     pg.display.update()
#     clock.tick(60)
#
# pg.quit()
# sys.exit()

# asciify.external_asciify(img_url)

# print(f"Hitchhiker's Guide to the Galaxy query: {search_terms}")
# hg2g_search = f"HG2G entry location: {wiki_url}"
# print(hg2g_search)
# print("-" * len(hg2g_search))
# print(title)
# for i in summary:
#     print(i)
# loading=list("Downloading Image.................................................................")
# for i in loading:
#     print(i, end="")
#     sleep(0.005)
#     print("")
