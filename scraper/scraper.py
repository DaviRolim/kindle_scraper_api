import os

from repository.highlight_repository import HighlightRepository
from webbot import Browser
import time
import json

class Scraper:

    def __init__(self, url):
        show_window = True
        if os.getenv('ENVIRONMENT') == 'prod':
            show_window=False
        self.web = Browser(showWindow=show_window) # easier debugging
        self.url = url

    
    def login(self, email, password):
        self.web.go_to(self.url)
        self.web.type(email, id='ap_mail')
        self.web.type(password, id='ap_password')
        self.web.press(self.web.Key.ENTER)

    def extract_books_element(self):
        return self.web.find_elements(classname='kp-notebook-library-each-book')


    def extract_book_info(self, book_element):
        # TODO Time things, what is taking more time to complete? Probably the extract_highlights.
        # If so, find a way to improve the time
        book_element.click()
        time.sleep(4)
        title = self.extract_title()
        print(title)
        author = self.extract_author()
        print(author)
        last_accessed = self.extract_last_accessed()
        img = self.extract_image_url()
        print(img)
        # TODO check if last_accessed is greater than [last sync] if not, dont need to get the highlights
        # and then just return nothing (NOT PRIORITY NOW)
        highlights = self.extract_highlights()
        return {'title': title,
                'highlights': highlights,
                'author': author,
                'imageURL': img,
                'last_accessed': last_accessed}

    def extract_highlights(self):
        elements = self.web.find_elements(id='highlight')
        highlights = []
        for e in elements:
            highlights.append(e.text)
        return highlights

    def extract_image_url(self):
        elements = self.web.find_elements(tag='img')
        book_img = elements[-1].get_attribute('src')
        return book_img
    
    def extract_title(self):
        title = self.web.find_elements(tag='p', classname='kp-notebook-metadata')[2].text
        return title

    def extract_author(self):
        author_name = self.web.find_elements(tag='p', classname='kp-notebook-metadata')[1].text
        return author_name
        
    def extract_last_accessed(self):
        last_accessed = self.web.find_elements(id='kp-notebook-annotated-date')[0].text
        return last_accessed
