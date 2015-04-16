"""
This is a resource class which represents sentiment.
"""
class Sentiment(object):

	def __init__(self, zipcode, positive_sentiment_count, negative_sentiment_count, start_time, end_time):
		self.zipcode = zipcode
		self.positive_sentiment_count = positive_sentiment_count
		self.negative_sentiment_count = negative_sentiment_count
		self.start_time = start_time
		self.end_time = end_time

 	"""
	This method returns Sentiment object when you pass a sentiment dictionary
	"""	
	@classmethod	
	def from_dict(cls, dct):
		return cls(
			dct.get("zipcode"),
			dct.get("positive_sentiment_count"),
			dct.get("negative_sentiment_count"),
			dct.get("start_time"),
			dct.get("end_time"),
		)


	"""
	This method creates sentiment dictionary from a given sentiment object
	"""
	def to_dict(self):
		return {
			"zipcode": self.zipcode,
			"positive_sentiment_count": self.positive_sentiment_count,
			"negative_sentiment_count": self.negative_sentiment_count,
			"start_time": self.start_time,
			"end_time": self.end_time,
		}	
