import json
from random import sample
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
import boto3

client = boto3.client('lambda')

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


def get_user_streak(user_ref):
    user_doc = user_ref.get()
    user = user_doc.to_dict()
    return user['streak']


def response_ok(streak):
    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "charset": "utf-8"},
        'body': {'streak': streak}
    }


def handler(event=None, context=None):
    print(event)
    users_docs = db.collection(u'users').get()
    for doc_id in users_docs:
        print(doc_id.id)
        print(doc_id.to_dict())
        payload = { "queryStringParameters": { "id":doc_id.id}}
        client.invoke(
                    FunctionName='dailyhighlights',
                    InvocationType='Event',  # 'RequestResponse',
                    Payload=json.dumps(payload)
                )
    
    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "charset": "utf-8"},
        'body': {'message': "Success"}
    }
