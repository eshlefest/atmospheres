# atmospheres
868 Term Project
Webapp to categorize and display happiness in San Francisco according to real-time tweets.

![](https://github.com/eshlefest/atmospheres/blob/master/capture.jpg)

Backend:
  Ryan and Sweta

Angular hackers
  vishal, vidya, sammy

data-viz:
  Eric, Harini

  link to  ProductBacklog:  https://docs.google.com/spreadsheets/d/1JBswpF0NF2fyiuDTSWsKhXERHPxPgBGJPuK2QpmGLPw/edit#gid=0


## Requirements & Dependencies
Python dependencies for the backend include:

 1. tweepy
 2. nltk
 3. pymongo
 4. flask

Machine should also have a running instance of Mongodb. To install  Mongo db follow the instruction [given here](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/)

## Installation
Checkout the source code and run the following command from the root directory of project. It is recommended to install python
virtual environment and then run the following command.

if you dont have git installed:

``sudo apt-get install git``

clone the repo:

``git clone https://github.com/eshlefest/atmospheres.git``

Install pip: ``sudo easy_install pip``

``pip install -e . -U``

download NLTK stopwords corpoora:
``sudo python -m nltk.downloader``
* click on "Corpora" tab
* scroll down, click on 'stopwords'
* click 'download'

## Running

### Start Reading and Recording Tweets
update atmospheres/ingestion/properties.py with the twitter API keys
* these keys are shared in a google document, if you cant access it, let Ryan know

Make sure your MongoDB instance is running.  Execute the following command from project root directory:
``atmospheres-ingest``
After several seconds, you should see tweets and their sentiment printed to the console.  They are also being stored in the DB.

### Start the Web Server
Just run the following command on the console from root directory of project ie, next to setup.py. If you have virtual enviroment then run it inside virtual environment.
``atmospheres-web-service``
Once the application is running you will see the following log line on the console.
``
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 ``
 To test the webservice hit the http://127.0.0.1:5000/ on web-browser.
