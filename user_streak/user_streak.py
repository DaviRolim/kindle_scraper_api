import json
from random import sample
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta


cred = credentials.Certificate('./freeadwise-0324a980ef62.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def date_to_str(date):
    return date.strftime('%d-%m-%Y')


def str_to_date(date_str):
    return datetime.strptime(date_str, '%d-%m-%Y')

def _get_user_ref(userID):
    doc_ref = db.collection(u'users').document(userID)
    return doc_ref
def _get_today_highlights_ref(user_ref):
    today_date_str = date_to_str(datetime.now().date())
    daily_highlight_ref = user_ref.collection(
        u'daily-highlights').document(today_date_str)

    return daily_highlight_ref

def _get_yesterday_highlights_ref(user_ref):
    yesterday_date_str = date_to_str(datetime.now().date() - timedelta(days=1))
    yesterday_highlight_ref = user_ref.collection(
        u'daily-highlights').document(yesterday_date_str)

    return yesterday_highlight_ref

def handler(event=None, context=None):
    print(event)
    userID = event['queryStringParameters']['id']
    user_ref = _get_user_ref(userID)
    
    # Getting today document
    today_doc = _get_today_highlights_ref(user_ref)

    doc_daily_review = today_doc.get()
    today_review = doc_daily_review.to_dict()


    # Getting yesterday document
    doc_yesterday = _get_yesterday_highlights_ref(user_ref)

    doc_yesterday = doc_yesterday.get()
    yesterday_review = doc_yesterday.to_dict()

    request_method = event['requestContext']['http']['method']
    if request_method == 'GET':
        if (yesterday_review['finished'] and not today_review['finished']):
             user_ref.update({'streak': 1})
        elif (not yesterday_review['finished'] and not today_review['finished']):
             user_ref.update({'streak': 0})

    if request_method == 'POST':
        today_doc.set({'finished': True}, merge=True)
        if yesterday_review['finished']:
            user_ref.update({'streak': firestore.Increment(1)})
        else:
            user_ref.update({'streak': 1})
    user_doc = user_ref.get()
    user = user_doc.to_dict()
    streak = user['streak']

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "charset": "utf-8"},
        'body': {'streak': streak}
    }
