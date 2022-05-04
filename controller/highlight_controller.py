from scraper.scraper import Scraper
from repository.remote_repository import RemoteRepository
from repository.highlight_repository import HighlightRepository, LocalRepository
from adapters.scrapper_to_db import adapt_scrapped_book_to_internal
import time

class HighlightController:
    def __init__(self, is_local=False):
        if is_local:
            self.repository = LocalRepository()
        else:
            self.repository = RemoteRepository()

    def get_highlight(self, user, number_of_quotes=5):
        return self.repository.get_random_highlights(user, number_of_quotes)

    def sync_books(self, email, password, username):
        scraper = Scraper('https://read.amazon.com/notebook')

        scraper.login(email, password)
        time.sleep(4)

        books_element = scraper.extract_books_element()
        time.sleep(2)

        books_scrapped = self._get_all_books_information(books_element, scraper)

        books_internal = list(map(adapt_scrapped_book_to_internal, books_scrapped))
        self.repository.save_books(books_internal, username)
        print("done")

    def _get_all_books_information(self, books_element, scraper):
        books_scrapped = []
        for book_element in books_element[1:]:
            try:
                book_info = scraper.extract_book_info(book_element)
                books_scrapped.append(book_info)

                time.sleep(1)
            except Exception as e:
                print(e)
        return books_scrapped