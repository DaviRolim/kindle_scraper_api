import os
from random import sample
from datetime import datetime

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

    def save_books(self, books: str, user: str):
        # TODO I can make every book be a collection so each highlight is one document
        # To add functionalities later like Favorite highlights
        # it would be hard in this current model, because the
        books_lenght = len(books)
        doc_ref = self.db.collection(u'user').document(user)
        meta_doc = doc_ref.collection(u'info').document('meta')
        meta_doc.set({
            'last_sync': datetime.now(),
            'total_books': books_lenght})

        books_ref = doc_ref.collection(u'books')
        for book in books:
            book_ref = books_ref.document(book['title'])
            book_ref.set({'last_accessed': book['last_accessed'],
                          'author' : book['author'],
                          'imageURL': book['imageURL']})
            book_highlights_ref = book_ref.collection(u'highlights')
            for highlight in book['highlights']:
                book_highlights_ref.add(highlight)

    def get_random_highlights(self, user, number_of_quotes: int):
        # TODO make this work for the new layout of documents.
        doc_ref = self.db.collection(u'user').document(user)
        books_collection = doc_ref.collection(u'books').stream()
        books_list = []
        for doc in books_collection:
            highlights = doc.to_dict()['highlights']
            for highlight in highlights:
                books_list.append({doc.id: highlight})

        return sample(books_list, number_of_quotes)

    def get_book(self, user):
        pass