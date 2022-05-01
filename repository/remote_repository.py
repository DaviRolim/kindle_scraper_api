import os
from random import sample
from itertools import chain

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from repository.highlight_repository import HighlightRepository
from dotenv import load_dotenv

load_dotenv()


class RemoteRepository(HighlightRepository):

    def __init__(self):
        cred = credentials.Certificate(os.getenv('FIRESTORE_CREDENTIALS_PATH'))
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_highlights(self, highlights: str, user: str):
        for book_name, book_higlights in highlights.items():
            doc_ref = self.db.collection(u'user').document(user)
            book_ref = doc_ref.collection(u'books').document(book_name)
            book_ref.set({
                u'metadata': {u'name': book_name},
                u'highlights': book_higlights
            })
    def get_highlight(self, number_of_quotes: int):
        doc_ref = self.db.collection(u'user').document('Davi Holanda')
        books_collection = doc_ref.collection(u'books').stream()
        books_list = []
        # TODO bring only [number_of_quotes] of random books from firestore 
        # to reduce the number of times in the loop.
        for doc in books_collection:
            highlights = doc.to_dict()['highlights']
            for highlight in highlights:
                books_list.append({doc.id: highlight})
        print(books_list[0])

        return sample(books_list, number_of_quotes)
