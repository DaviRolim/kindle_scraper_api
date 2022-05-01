from repository.highlight_repository import HighlightRepository
from webbot import Browser
import time
import json

class Scraper:

    def __init__(self, url):
        self.web = Browser(showWindow=True) # easier debugging
        self.url = url

    
    def login(self, username, password):
        self.web.go_to(self.url)
        self.web.type(username, id='ap_mail')
        self.web.type(password, id='ap_password')
        self.web.press(self.web.Key.ENTER)

    def extract_books(self):
        h2s = self.web.find_elements(tag='h2')
        books = []
        for h in h2s:
            books.append(h.text)
        return books

    def extract_highlights(self,book):
        if self._book_contains_single_quote(book):
            self.web.click(xpath=f'//body//button[@value=\"{book}\"]')
        else:
            self.web.click(book)

        elements = self.web.find_elements(id='highlight')
        highlights = []
        for e in elements:
            highlights.append(e.text)
        return highlights
    
    def _book_contains_single_quote(self, book: str):
        return "'" in book
