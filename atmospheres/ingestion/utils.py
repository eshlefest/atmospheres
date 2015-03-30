import pickle
from mongoreader import MongoReader
from properties import *


def get_mongo_reader():
    """Returns an instance of the MongoBridge that is connected to the 
       database defined in properties.py """
    return MongoReader(DATABASE_NAME,COLLECTION_NAME)

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
    return unpickle_object(CLASSIFIER_FILE), unpickle_object(CLASSIFIER_FEATURES)

def pickle_classifier(classifier):
    """ saves the classifier to the location defined in properties.py """
    pickle_object(classifier.classifier, CLASSIFIER_FILE)
    pickle_object(classifier.all_words,CLASSIFIER_FEATURES)


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

