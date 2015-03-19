import pickle
from mongoreader import MongoBridge
from properties import *


def get_mongo_bridge():
    return MongoBridge(DATABASE_NAME,COLLECTION_NAME)

def get_twitter_properties():
    properties = {}

    properties["access_token"] = access_token
    properties["access_token_secret"] = access_token_secret
    properties["consumer_key"] = consumer_key
    properties["consumer_secret"] = consumer_secret

    return properties


def get_pickled_classifier():
    return unpickle_object(CLASSIFIER_FILE), unpickle_object(CLASSIFIER_FEATURES)

def pickle_classifier(classifier):
    pickle_object(classifier.classifier, CLASSIFIER_FILE)
    pickle_object(classifier.all_words,CLASSIFIER_FEATURES)


def pickle_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def unpickle_object(filename):
    f = open(filename, 'r')
    obj = pickle.load(f)
    f.close()
    return obj    

