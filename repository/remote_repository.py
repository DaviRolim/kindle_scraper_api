import os
from random import sample

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from repository.highlight_repository import HighlightRepository
from dotenv import load_dotenv

load_dotenv()


class RemoteRepository(HighlightRepository):

    def __init__(self):
        # Use the application default credentials
        # Deploy on GCP server
        if os.getenv('ENVIRONMENT') == 'prod':
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred, {
            'projectId': 'freeadwise',
            })
        # Deploy on my own server (local) using the certificate
        else:
            cred = credentials.Certificate(os.getenv('FIRESTORE_CREDENTIALS_PATH'))
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_highlights(self, highlights: str, user: str):
        # TODO when saving highlights, update a doc in the user/meta
        # with the last sync date and total books [len(highlights)]
        # TODO instead of using the name of the book as doc id
        # use a number starting from 1 to ... and put the name of the book and author
        # as a field in the document.
        # TODO instead of a list of strings with the highlights,
        # return a list of dictionaries with the location and highlight
        for book_name, book_higlights in highlights.items():
            doc_ref = self.db.collection(u'user').document(user)
            book_ref = doc_ref.collection(u'books').document(book_name)
            book_ref.set({
                u'metadata': {u'name': book_name},
                u'highlights': book_higlights
            })
    def get_random_highlights(self, user, number_of_quotes: int):
        doc_ref = self.db.collection(u'user').document(user)
        books_collection = doc_ref.collection(u'books').stream()
        books_list = []
        # TODO bring only [number_of_quotes] of random books from firestore 
        # to reduce the number of times in the loop.
        for doc in books_collection:
            highlights = doc.to_dict()['highlights']
            for highlight in highlights:
                books_list.append({doc.id: highlight})

        return sample(books_list, number_of_quotes)
