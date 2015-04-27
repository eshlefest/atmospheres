from dateutil import parser
from tweetreader import TweetStreamReader
from utils import get_twitter_properties, get_mongo_reader
from senticlassifier import SentiClassifier
from tweepy import OAuthHandler
from tweepy import Stream
import json

from atmospheres.models.tweet import Tweet
from atmospheres.ingestion.utils import get_zipcode

db = get_mongo_reader()
classifier = SentiClassifier()

san_francisco = [-122.529439, 37.688995, -122.358464, 37.839899]

#lower left: 37.688995, -122.529439
# upper right: 37.839899, -122.358464

def on_tweet_received_callback(data):
    """ this function will be set as the callback function for the tweet reader, will be passed
        the tweet as an argument.
        it classifies the text, then saves the necessary info to the db
    """
    data = json.loads(data)
    text = data["text"]
    sentiment = classifier.classify(text)

    try:
        coords = data["geo"]["coordinates"]
    except:
        coords = None

    
    if coords and coords[0] and coords[1]:
        zipcode = get_zipcode(coords[1], coords[0])
    else:
        zipcode = None

    tweet = Tweet(
        None,  # Id 
        text, 
        sentiment,
        zipcode,
        parser.parse(data["created_at"]),
        coords[0] if coords else None,
        coords[1] if coords else None,
    )

    db.write(tweet.to_dict())
    print "%s %10s: %s"%(zipcode, sentiment,text)


def main():
    classifier.load_pickled_classifier()

    twitter_properties = get_twitter_properties()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    r = TweetStreamReader()
    r.set_data_callback(on_tweet_received_callback)

    auth = OAuthHandler(twitter_properties["consumer_key"], twitter_properties["consumer_secret"])
    auth.secure = True
    auth.set_access_token(twitter_properties["access_token"], twitter_properties["access_token_secret"])
    stream = Stream(auth, r)

    # filters for tweets in the bounding box described by san_francisco
    while(True):
        try:
            stream.filter(locations=san_francisco)
        except ReadTimeoutError as e:
            print(" disconnected! \n reconnecting")
            stream = Stream(auth, r)
            stream.filter(locations=san_francisco)




if __name__ == '__main__':
    main()


    