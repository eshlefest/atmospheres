"""
This is a resource class which represents sentiment.
"""
class Sentiment:

	def __init__(self, zipcode, positive_sentiment, negative_sentiment, start_time, end_time):
		self.zipcode = zipcode
		self.positive_sentiment = positive_sentiment
		self.negative_sentiment = negative_sentiment
		self.start_time = start_time
		self.end_time = end_time

	@classmethod	
	def from_dict(cls, dct):
		return cls(
			dct.get("zipcode"),
			dct.get("positive_sentiment"),
			dct.get("negative_sentiment"),
			dct.get("start_time"),
			dct.get("end_time"),
		)


	def to_dict(self):
		return {
			"zipcode": self.zipcode,
			"positive_sentiment": self.positive_sentiment,
			"negative_sentiment": self.negative_sentiment,
			"start_time": self.start_time,
			"end_time": self.end_time,
		}	
