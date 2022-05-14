import json
from random import sample
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime


cred = credentials.Certificate('./freeadwise-0324a980ef62.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def date_to_str(date):
    return date.strftime('%d-%m-%Y')


def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')


def _generate_random_highlights(user, number_of_quotes: int = 10):
    # TODO make this work for the new layout of documents.
    doc_ref = db.collection(u'users').document(user)
    books_collection = doc_ref.collection(u'books').stream()
    books_list = []
    for doc in books_collection:
        book_dict = doc.to_dict()
        book_title = doc.id
        highlights = book_dict['highlights']
        author = book_dict['author']
        imageURL = book_dict['imageURL']
        for highlight in highlights:
            books_list.append(
                {'title': book_title, 'highlight': highlight, 'author': author, 'imageURL': imageURL})

    return sample(books_list, number_of_quotes)

def _get_daily_highlights_ref(userID):
    doc_ref = db.collection(u'users').document(userID)
    today_date_str = date_to_str(datetime.now().date())
    daily_highlight_ref = doc_ref.collection(
        u'daily-highlights').document(today_date_str)

    return daily_highlight_ref

def _setupDailyHighlights(daily_highlight_ref, userID):
    random_highlights = _generate_random_highlights(userID)
    response = {'quotes': random_highlights}
    
    daily_highlight_ref.set(response)

    return response

def handler(event=None, context=None):
    userID = event['queryStringParameters']['id']

    daily_highlight_ref = _get_daily_highlights_ref(userID)
    doc = daily_highlight_ref.get()
    if doc.exists:
        response = doc.to_dict()
    else:
        response = _setupDailyHighlights(daily_highlight_ref, userID)
        
    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "charset": "utf-8"},
        'body': response
    }
