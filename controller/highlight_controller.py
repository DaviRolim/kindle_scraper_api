from scraper.scraper import Scraper
from repository.remote_repository import RemoteRepository
from repository.highlight_repository import HighlightRepository, LocalRepository
import time

class HighlightController:
    def __init__(self, repository: HighlightRepository):
        self.repository = repository

    def get_highlight(self, number_of_quotes=5):
        return self.repository.get_random_highlights(number_of_quotes)

    def sync_highlights(self, username, password):
        scraper = Scraper('https://read.amazon.com/notebook')

        scraper.login(username, password)
        time.sleep(4)

        books = scraper.extract_books()
        time.sleep(3)

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

        self.repository.save_highlights(books_highlights, 'Davi Holanda')

        print("done")