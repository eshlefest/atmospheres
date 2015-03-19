#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from senticlassifier import SentiClassifier
from mongoreader import MongoBridge
from utils import get_twitter_properties

san_francisco = [-122.529439, 37.688995, -122.358464, 37.839899]

#lower left: 37.688995, -122.529439
# upper right: 37.839899, -122.358464

#This is a basic listener that just prints received tweets to stdout.
class TweetStreamReader(StreamListener):

    def __init__(this):
        this.classifier = SentiClassifier()
        this.mongo_bridge = MongoBridge()

    def on_data(self, data):
        self.data_callback(data)
        return True

    def on_error(self, status):
        print status

    def set_data_callback(self,func):
        self.data_callback = func



if __name__ == '__main__':

    twitter_properties = get_twitter_properties()

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = TweetStreamReader()
    auth = OAuthHandler(twitter_properties["consumer_key"], twitter_properties["consumer_secret"])
    auth.set_access_token(twitter_properties["access_token"], twitter_properties["access_token_secret"])
    stream = Stream(auth, l)

    # filters for tweets in the bounding box described by san_francisco
    stream.filter(locations=san_francisco)