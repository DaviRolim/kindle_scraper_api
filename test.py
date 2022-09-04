import json
from random import sample
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
import time


cred = credentials.Certificate('./freeadwise-0324a980ef62.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def date_to_str(date):
    return date.strftime('%d-%m-%Y')


def create_sync_document(user_ref, total_books):
    sync_ref = user_ref.collection(u'sync')
    sync_doc = sync_ref.add(
        {
            # TODO I could add a field "new books" subtracting the total with the current total in the user sync
            'startTime': firestore.SERVER_TIMESTAMP,
            'totalBooks': total_books,
            'updatedBooks': 0
        }
    )
    return sync_doc


def update_last_sync(sync_doc):
    sync_doc.update({u'updatedBooks': firestore.Increment(1)})

def finished_sync(sync_doc):
    sync_doc.update({u'endTime': firestore.SERVER_TIMESTAMP})
    
def handler():
    users_docs = db.collection(u'users').get()
    for doc_id in users_docs:
        print(doc_id.id)
        print(doc_id.to_dict())
    # user_doc = user_ref.get()
    # user = user_doc.to_dict()
    # return streak

handler()
# for doc in docs:
#     print(f'{doc.id}')

