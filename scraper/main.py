from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta

from tempfile import mkdtemp
import boto3
import json

client = boto3.client('lambda')

options = webdriver.ChromeOptions()
options.binary_location = '/opt/chrome/chrome'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280x1696")
options.add_argument("--single-process")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-dev-tools")
options.add_argument("--no-zygote")
options.add_argument(f"--user-data-dir={mkdtemp()}")
options.add_argument(f"--data-path={mkdtemp()}")
options.add_argument(f"--disk-cache-dir={mkdtemp()}")
options.add_argument("--remote-debugging-port=9222")


# Initializing firestore
cred = credentials.Certificate('./freeadwise-0324a980ef62.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def str_to_date(date_string):
    return datetime.strptime(date_string, '%A %B %d, %Y').date()

def get_last_sync_date(user_id):
    doc_ref = db.collection(u'user').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        doc_dict = doc.to_dict()
        last_sync = doc_dict['last_sync']
        date = datetime.fromtimestamp(last_sync.timestamp())
        return date.date()
    # if user is not yet created, last_sync will be 300 years ago
    return (datetime.now() - timedelta(days=365*300)).date()

def update_user_metadata(user_id, total_books):
    user_ref = db.collection(u'user').document(user_id)
    
    user_ref.set({
            'last_sync': datetime.now(),
            'total_books': total_books})

# TODO Create exception classes so I can refactor the code and raise proper errors and keep the handler cleaner.

def extract_highlights(soup):
    elements = soup.find_all('span', id='highlight')
    highlights = []
    for element in elements:
        highlights.append({'highlight':  element.get_text(), 'isFavorite': False})
    return highlights

def input_valid(body):
    required_keys = ['username', 'email' , 'password']
    if all(key in body for key in required_keys):
        return True

def handler(event=None, context=None):
    print(event)
    body = json.loads(event['body'])
    # TODO add firestore here to update the last_sync before return the result (if everything goes ok and highlights are synced)
    # and to check if the [lastAccessed] property is before the last synced, if this is the case I don't need to call the second lambda

    # Check if input contains the required keys before continuing
    if not input_valid(body):
        return {
            "statusCode": 400,
            "body": {"message": "Make sure you're sending 'email', 'password' and 'username' in the request body"}
        }
        
    # Get the parameters from the event
    email = body['email']
    password = body['password']
    username = body['username']

    # Start the chrome driver using the options above
    chrome = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    
    # Connect to the Kindle webpage
    chrome.get("https://read.amazon.com/notebook")

    # Wait until the element containing the input for email appear on the screen
    WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email")))
    # Login
    chrome.find_element_by_id('ap_email').send_keys(email)
    chrome.find_element_by_id('ap_password').send_keys(password)
    chrome.find_element_by_id('signInSubmit').click()

    # Wait until the page is loaded and the elements area appearing on the screen
    try:
        WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "kp-notebook-library-each-book")))
         # Find all clickable book elements to iterate
        books_elements_to_click = chrome.find_elements_by_class_name(
            'kp-notebook-library-each-book')
        total_books = len(books_elements_to_click)
        print(f'Number of books {total_books}')

        last_sync_date = get_last_sync_date(username)
        # For each book, extract the information and send to the second lambda that will load to firestore
        for book_el in books_elements_to_click: 
            try:
                # Go to the book page with its highlights and information
                book_el.click()
                
                # Wait until the elements appear on the screen
                WebDriverWait(chrome, 10).until(
                    EC.presence_of_element_located((By.ID, "annotation-scroller")))
                
                # Get the HTML content of the page
                content = chrome.page_source
                
                # Initialize BeautifulSoup to scrap the content of the page, as BS is way faster than selenium for this purpose.
                soup = BeautifulSoup(content, features="html.parser")
                main_div = soup.find('div', {'class': 'kp-notebook-annotation-container'})
                header_div = main_div.findChild('div')

                # Gather the elements I need
                title = header_div.find_next('h3').get_text().strip()
                imgURL = header_div.find_next('img').attrs['src']
                last_accessed = header_div.find_next(
                    'span', id='kp-notebook-annotated-date').get_text().strip()
                author = header_div.find_all_next('p')[1].get_text().strip()
                highlights = extract_highlights(soup)

                # Books links are ordered by last accessed by default.
                # So if the last_sync date is greater than lascAccessed
                # I can break out of this loop
                last_acessed_date = str_to_date(last_accessed)
                if last_sync_date > last_acessed_date:
                    break
                
                book_info = {'username': username,
                            'title': title,
                            'author': author,
                            'imageURL': imgURL,
                            'lastAccessed': last_accessed,
                            'highlights': highlights}
                # Call the second lambda that saves this to firestore
                client.invoke(
                    FunctionName = 'firestore-db',
                    InvocationType = 'Event', #'RequestResponse',
                    Payload = json.dumps(book_info)
                )

            except Exception as e:
                print(e)
                return {
                    "statusCode": 500,
                    "body": {"message": "Could not syncronize your highlights"}
                }
        # Before returning with success, save user metadata on firestore
        update_user_metadata(username, total_books)
        return {
            "statusCode": 200,
            "body": {"message": "Highlights Syncronized"}
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 401,
            "body": {"message": "Make sure your email and password are valid in order to connect to read.amazon.com/notebook"}
        }


   
