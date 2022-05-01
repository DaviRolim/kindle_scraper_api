from scraper.scraper import Scraper
from repository.remote_repository import RemoteRepository
from repository.highlight_repository import LocalRepository
import time

class HighlightAPI:
    repository = LocalRepository()
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