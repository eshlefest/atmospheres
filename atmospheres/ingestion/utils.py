import pickle
from os import path
from shapely.geometry import Polygon, Point

from atmospheres.db.datastore import DataStore
from properties import *
from atmospheres.controller.geo_json import sf_geo_json


# this will be a list of (Polygon,zip_code) tuples
zip_polygons = []

# populate shapely polygon list
for feature in sf_geo_json["features"]:
    polygon = Polygon(feature["geometry"]["geometries"][0]["coordinates"][0])
    zip_code = feature["id"]
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




