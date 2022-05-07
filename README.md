# Kindle Scraper with Serverless - Lambda

## The Solution
Here we have two Lambda functions using container images. Let's understand about each one of these functions.
- The first lambda is the entrypoint that should receive the request and expects a body as follows:
```json
{
    "username": "username_that_will_be_used_in_database",
    "email": "email_to_conect_to_your_kindle_account",
    "password": "password_to_conect_to_your_kindle_account"
}
```
_I know, using email and password in a body request isn't safe, this is the first version._  

This first function will open a browser, connect to kindle highlights webpage and scrap the page of each book and gather the following information.
```json
{
    "title": "Title of the book",
    "author": "Author of the book",
    "imageURL": "Author of the book",
    "lastAccessed": "Last time you accessed the book in your kindle",
    "highlights": ["a list", "with all your highlights"]
}
```
I'm sending this result to
- The second Lambda function, that is responsible to saving this using Firestore. So you can consume later on your app or webpage. 
  
If you just want the whole json returned, you can instead of calling the second lambda function with the payload, you can create a list, add all results to that list and then returning this list. (Keep in mind that the payload might be bigger than the max size allowed for a lambda function, as a workaround you can compress the response using gzip or zlib).


The image used to open chrome with selenium goes with these versions. [These are automatically updated and tested everyday. ![CircleCI](https://circleci.com/gh/umihico/docker-selenium-lambda/tree/circleci.svg?style=svg)](https://circleci.com/gh/umihico/docker-selenium-lambda/tree/circleci)


## Setup
In order to run and upload to lambda will you need.
- AWS account setup and a ~.aws/credentials configured.
- (Optional) If you want to use firestore to load your highlights, you'll need a google cloud account and the credentials for the project, so you can use to replace the hardcoded json file used in the credentials part of the function. _If you don't want to use firestore, remove the firebase_repo directory and the code parts relating to firebase in the scraper function.
- Install serverless framework.  

## Running the demo

```bash
$ npm install -g serverless # skip this line if you have already installed Serverless Framework
$ export AWS_REGION=ap-northeast-1 # You can specify region or skip this line. us-east-1 will be used by default.
$ git clone https://github.com/DaviRolim/kindle_scraper_api.git
$ sls deploy
$ sls invoke --function scraper # Yay! You will get texts of example.com
```
