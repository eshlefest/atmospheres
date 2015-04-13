"""
This class is model class. Basically used to store data.
"""
class Tweet:

	def __init__(self, id, tweet_text, sentiment, zipcode, created, latitude, longitude):
		self.id = id
		self.sentiment = sentiment
		self.zipcode = zipcode
		self.tweet_text = tweet_text
		self.created = created
		self.latitude = latitude
		self.longitude = longitude

	@classmethod
	def from_dict(cls, dct):
		return cls(
			dct.get("id"),
			dct.get("tweet_text"),
			dct.get("sentiment"),
			dct.get("zipcode"),
			dct.get("created"),
			dct.get("latitude"),
			dct.get("longitude"),
		)

	def to_dict(self):
		return { 
			"id": self.id, 
			"tweet_text": self.tweet_text, 
			"sentiment": self.sentiment,
			"zipcode": self.zipcode,
			"created": self.created,
			"latitude": self.latitude,
			"longitude": self.longitude,
		}	
