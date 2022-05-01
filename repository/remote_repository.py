import os

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
