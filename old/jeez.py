# Need to write exceptions for disambiguation, wiktionary, file instances
# wiktionary: fuck a duck || disambiguation: GFY || file: evoluti

import scrapy
import atexit
import re
import os
import json
from scrapy.linkextractors import LinkExtractor

@atexit.register
def goodbye():
    if url:
        print(f"Here's your link: {url}")
    else:
        print("Something broke, dude. Sorry.")

input = input("Which wiki you want?> ")
search_terms = input.replace(' ', '+')
print(f"Search term is: {search_terms}")

class GoogleFirstResult(scrapy.Spider):
    name = 'googscraper'
    start_urls = ['https://www.google.com/search?q=site:https://en.wikipedia.org/+' + search_terms]

    def parse(self, response):
        global url
        try:
            result = response.xpath('//a[contains(@href,"https://en.wikipedia.org/wiki/")]').get()
            print(f"RESULT: {result}")
            url_regex = re.compile(r'https://en.wikipedia.org/wiki/[^&]*')
            special_char_regex = re.compile(r'%[0-9]*')
            stript = url_regex.search(result).group()
            print(f"URL Stripped: {stript}")
            if special_char_regex.search(stript):
                chars_to_cut = special_char_regex.search(stript).group()
                print(f"Special Chars to be Removed: {chars_to_cut}")
                stript = stript.replace(chars_to_cut, "")
            url = stript
        except:
            url = "Looks like there aren't any great matches for your search"
