from mongoreader import MongoBridge
import nltk, random, re, string
from nltk.classify import apply_features
from nltk.stem.porter import *
from nltk.corpus import stopwords
import argparse

from utils import get_pickled_classifier

TEST_SET_PROPORTION = .1


class SentiClassifier():

    def __init__(self):
        self.reader = MongoBridge()
        self.regex = re.compile('[%s]' % re.escape(string.punctuation))
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))


    def train(self, num_samples):
        """uses connection to mongodb to read in tweets that contain :) and :(
            the size of the training data is 2 * num_samples"""
        
        print "Querying DB"
        # read samples from DB
        posTweets = self.reader.get_N_results("\\:\\)",num_samples)
        negTweets = self.reader.get_N_results("\\:\\(",num_samples)
        
        print "Query Returned"
        # read query results into memory
        posTweets = [(t["text"].split(" "),'positive') for t in posTweets]
        negTweets = [(t["text"].split(" "),'negative') for t in negTweets]

        labeled_tweets = posTweets + negTweets

        random.shuffle(labeled_tweets)

        print "compiling all words list"
        # extract all unique words from the tweets
        # these will be used as features
        self.all_words = self.get_all_words(labeled_tweets)

        # remove stop words
        self.all_words = self.all_words.difference(self.stop_words)
        print "num words: %d"%len(self.all_words)
        
        test_size = int(len(labeled_tweets) * TEST_SET_PROPORTION)

        # apply_features is a lazy loader, so that features are
        # computed as necessary, instead of being loaded into memory
        # all at once
        train_set = apply_features(self.document_features,labeled_tweets[:len(labeled_tweets) - test_size])
        test_set = apply_features(self.document_features,labeled_tweets[len(labeled_tweets) - test_size:])
        
        
        print "training"
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        
        #print accuracy on test set
        print "Accuracy on "
        print(nltk.classify.accuracy(self.classifier, test_set))

    def get_all_words(self,labeled_tweets):
        """ returns a set of all unique words """
        tweets = [t for t,polarity in labeled_tweets]
        all_words = [] 
        for t in tweets:
            all_words += [self.preprocess_word(w) for w in t]
        
        return set(all_words)

    def classify(self,text):
        """runs the classifier on the input text """
        document = text.split(" ")
        features = self.document_features(document)
        return self.classifier.classify(features)

    def document_features(self,document): 
        """ extracts the features from the input document """
        document_words = set(document)
        features = {}
        for word in self.all_words:
            features['contains(%s)' % word] = (self.preprocess_word(word) in document_words)
        return features

    def preprocess_word(self,word):
        """ this method does 3 preprocessing steps:
            1.  gets rid of all punctiation as defined in the python string library
                punctionarion includes: '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            2.  case folding, (everything in lowercase)
            3.  Stemming using the Porter Stemmer included in the
                Python Natural Language Toolkit (NLTK) """

        w = self.regex.sub('',word)
        return self.stemmer.stem(w.lower())

    def load_pickled_classifier(this):
        """ sets the classifier and features list to the serialized classifier in properties.py """
        this.classifier, this.all_words = get_pickled_classifier()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sentiment classifier')
    parser.add_argument('train_size', type=int)
    args = parser.parse_args()


    c = SentiClassifier()
    
    #c.train(args.train_size)
    c.load_pickled_classifier()
    print c.classify("San francisco tomorrow night for #dirtytalk I get to see so many awesome folks #yay")













