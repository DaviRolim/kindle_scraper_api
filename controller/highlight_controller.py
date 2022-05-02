from scraper.scraper import Scraper
from repository.remote_repository import RemoteRepository
from repository.highlight_repository import HighlightRepository, LocalRepository
import time

class HighlightController:
    def __init__(self, is_local=False):
        if is_local:
            self.repository = LocalRepository()
        else:
            self.repository = RemoteRepository()

    def get_highlight(self, user, number_of_quotes=5):
        return self.repository.get_random_highlights(user, number_of_quotes)

    def sync_highlights(self, email, password, username):
        scraper = Scraper('https://read.amazon.com/notebook')

        scraper.login(email, password)
        time.sleep(4)

        books = scraper.extract_books()
        time.sleep(3)

        books_highlights = self._get_highlights_for_all_books(books, scraper)
        # TODO change email in the params for email and get another field called email
        # to change the hard coded string below.
        self.repository.save_highlights(books_highlights, username)
        print("done")

    def _get_highlights_for_all_books(self, books, scraper):
        books_highlights = {}
        for book in books:
            print("extracting highlights for " + book)
            try:
                highlights = scraper.extract_highlights(book)
                books_highlights[book] = highlights
                time.sleep(2)
            except Exception as e:
                print(e)
                print("could not extract highlights for: " + book)