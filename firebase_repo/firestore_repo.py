import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
# TODO add firebase_admin and put the file with credentials here
# transform this in a container and copy the credentials file there.


cred = credentials.Certificate('./freeadwise-0324a980ef62.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def handler(event=None, context=None):
    print(event['title'])
    doc_ref = db.collection(u'user').document(event['username'])
    book_ref = doc_ref.collection(u'books').document(event['title'])
    last_accessed_time = datetime.strptime(event['lastAccessed'], '%A %B %d, %Y')
    book_ref.set({'lastAccessed': last_accessed_time,
                  'author': event['author'],
                  'imageURL': event['imageURL'],
                  'highlights': event['highlights']})
    # book_highlights_ref = book_ref.collection(u'highlights')
    # for highlight in event['highlights']:
    #     book_highlights_ref.add(highlight)
