"""
This module contains resource classes for aggregated sentiment.
"""
class SentimentType(object):
	positive = "positive"
	negative = "negative"

class Sentiment(object):
	"""
	This is a resource class which represents sentiment.
	"""

	def __init__(self, zipcode, positive_sentiment_count, negative_sentiment_count, start_time, end_time):
		self.zipcode = zipcode
		self.positive_sentiment_count = positive_sentiment_count
		self.negative_sentiment_count = negative_sentiment_count
		self.start_time = start_time
		self.end_time = end_time

	@classmethod	
	def from_dict(cls, dct):
		"""
		This method returns Sentiment object when you pass a sentiment dictionary
		"""	
		return cls(
			dct.get("zipcode"),
			dct.get("positive_sentiment_count"),
			dct.get("negative_sentiment_count"),
			dct.get("start_time"),
			dct.get("end_time"),
		)
	
	def to_dict(self):
		"""
		This method creates Sentiment dictionary from a given Sentiment object
		"""
		return {
			"zipcode": self.zipcode,
			"positive_sentiment_count": self.positive_sentiment_count,
			"negative_sentiment_count": self.negative_sentiment_count,
			"start_time": self.start_time,
			"end_time": self.end_time,
		}	


class Sentiments(object):
	"""
	This is a resource class which represents list of sentiments.
	"""
	
	def __init__(self, zipcode_sentiment_map, start_time, end_time):
		"""
		Here zipcode_sentiment_map is a hashmap where zipcode is a key and value is a dictionary with 
		postive sentiments counts and negative sentiments counts. This is for a specified time period
		E.g 
			{
			94608: { positive_sentiment_count : 20, negative_sentiment_count: 10 }
			}
		"""
		self.zipcode_sentiment_map = zipcode_sentiment_map
		self.start_time = start_time
		self.end_time = end_time

	@classmethod	
	def from_dict(cls, dct):
		"""
		This method return Sentiments object from Sentiments dictionary.
		"""
		return cls(
			dct.get("zipcode_sentiment_map"),
			dct.get("start_time"),
			dct.get("end_time"),
		)

	def to_dict(self):
		"""
		This method creates Sentiments dictionary from a given Sentiments object
		"""
		return {
			"zipcode_sentiment_map": self.zipcode_sentiment_map,
			"start_time": self.start_time,
			"end_time": self.end_time,
		}
