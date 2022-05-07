from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from tempfile import mkdtemp
import boto3
import time
import json

client = boto3.client('lambda')
# different requirements for different lambdas
# https://www.serverless.com/plugins/serverless-python-individually
 
# TODO add another function that receives the response for the second lambda (book_info)
# and save to firestore.

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

def extract_highlights(soup):
    elements = soup.find_all('span', id='highlight')
    highlights = []
    for element in elements:
        highlights.append(element.get_text())
    return highlights

def handler(event=None, context=None):
    print(event)
    email = event['body']['email']
    password = event['body']['password']
    username = event['body']['username']
    chrome = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    chrome.get("https://read.amazon.com/notebook")
    WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email")))
    # Login
    chrome.find_element_by_id('ap_email').send_keys(email)
    chrome.find_element_by_id('ap_password').send_keys(password)
    chrome.find_element_by_id('signInSubmit').click()

    WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "kp-notebook-library-each-book")))
    # Find all clickable book elements to iterate
    books_elements_to_click = chrome.find_elements_by_class_name(
        'kp-notebook-library-each-book')
    res = []
    print(f'[LIFE ENJOYER] Number of books {len(books_elements_to_click)}')
    for book_el in books_elements_to_click:
        try:
            book_el.click()
            WebDriverWait(chrome, 10).until(
                EC.presence_of_element_located((By.ID, "annotation-scroller")))
            
            content = chrome.page_source
            soup = BeautifulSoup(content, features="html.parser")
            main_div = soup.find('div', {'class': 'kp-notebook-annotation-container'})
            header_div = main_div.findChild('div')
            title = header_div.find_next('h3').get_text().strip()
            imgURL = header_div.find_next('img').attrs['src']
            last_accessed = header_div.find_next(
                'span', id='kp-notebook-annotated-date').get_text().strip()
            author = header_div.find_all_next('p')[1].get_text().strip()
            highlights = extract_highlights(soup)
            book_info = {'username': username,
                        'title': title,
                        'author': author,
                        'imageURL': imgURL,
                        'lastAccessed': last_accessed,
                        'highlights': highlights}
            client.invoke(
                FunctionName = 'firestore-db',
                InvocationType = 'Event', #'RequestResponse',
                Payload = json.dumps(book_info)
            )

        except Exception as e:
            print(e)
    return {
        "statusCode": 200,
        "body": {"message": "Highlights Syncronized"}
    }
