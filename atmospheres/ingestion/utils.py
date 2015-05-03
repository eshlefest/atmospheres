import pickle
from os import path
from shapely.geometry import Polygon, Point
import datetime

from atmospheres.db.datastore import DataStore
from properties import *
from atmospheres.controller.geo_json import sf_geo_json
import random
from atmospheres.models.tweet import Tweet


# this will be a list of (Polygon,zip_code) tuples
zip_polygons = []
sf_zipcode_array = []
neighborhoods = []

# populate shapely polygon list
for feature in sf_geo_json["features"]:
    polygon = Polygon(feature["geometry"]["geometries"][0]["coordinates"][0])
    zip_code = feature["id"]
    sf_zipcode_array.append(str(zip_code))
    neighborhoods.append(feature["neighborhood"])
    zip_polygons.append((polygon,zip_code))






def get_mongo_reader():
    """Returns an instance of the MongoBridge that is connected to the 
       database defined in properties.py """
    return DataStore(DATABASE_NAME, COLLECTION_NAME)

def get_twitter_properties():
    """ returns a dictionary with the twitter api information defined in 
        properties.py """
    properties = {}

    properties["access_token"] = access_token
    properties["access_token_secret"] = access_token_secret
    properties["consumer_key"] = consumer_key
    properties["consumer_secret"] = consumer_secret

    return properties


def get_pickled_classifier():
    """ returns reads and unserializes the serialized classifier """
    return unpickle_object(path.dirname(__file__) + '/../../'+ CLASSIFIER_FILE), unpickle_object(path.dirname(__file__) + '/../../'+ CLASSIFIER_FEATURES)

def pickle_classifier(classifier):
    """ saves the classifier to the location defined in properties.py """
    pickle_object(classifier.classifier, CLASSIFIER_FILE)
    pickle_object(classifier.all_words, CLASSIFIER_FEATURES)


def pickle_object(obj, filename):
    """ serializes the object obj and saves it to the file filename """
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def unpickle_object(filename):
    """ unserializes the object in filename """
    f = open(filename, 'r')
    obj = pickle.load(f)
    f.close()
    return obj  

def get_zipcode(lon,lat):
    """
    returns the coresponding zipcode from the goJSON data, else 'unknown'
    """
    point = Point(lon,lat)

    for p in zip_polygons:
        if p[0].contains(point):
            return p[1]

def add_random_tweets_to_db(num_tweets,date_range):
    """
    This function will randomly generate num_tweets with uniformly distributed sentiment
    the dates of the tweets will range between now and N number of days ago.  N=date_range
    location of tweet is randomly chosen within the bounding box of SF

    TODO write remove_random_tweets function

    """
    hour_range = date_range * 24
    db = get_mongo_reader()

    for i in range(num_tweets):
        lat = random.uniform(37.688995,37.839899)
        lon = random.uniform(-122.529439,-122.358464)

        sentiment = "positive" if random.random() > .5 else "negative"
        hours_delta = random.uniform(0,hour_range)
        date = datetime.datetime.now() - datetime.timedelta(hours=hours_delta)
        
        tweet = Tweet(
            None,  # Id 
            "random_tweet %d"%i, 
            sentiment,
            get_zipcode(lon,lat),
            date,
            lat,
            lon,
        )
        db.write(tweet.to_dict())
        



    

#def get_zipcode(latitude, longitude):
#    """
#    This method uses pygeocoder to fetch the respective zipcode by reverse geocoding
#    """
#    result = Geocoder.reverse_geocode(latitude, longitude)
#    # Return none if the result is empty or None.
#    if result:
#       return result.postal_code
#    else:    
#        return None 




