from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 
from twitter_credentials import *

## Twitter Authenticator class ##
class Authenticator():
	"""Class that Authenticates your Twitter App"""

	def authenticate_twitter_app(self):
		"""Create and return your authentication token/object/instance"""
		auth = OAuthHandler(API_KEY, API_SECRET_KEY)
		auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
		return auth


## Twitter Streamer Class ##
class TwitterStreamer():
	"""Streaming live tweets"""

	def stream_tweets(self, filename, key_words):
		"""Method that handles twitter authentication and connection to the Twitter Streaming API"""
		listener = TwitterListener(filename)
		twitter_authenticator = Authenticator()
		auth = twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		stream.filter(track=key_words)


class TwitterListener(StreamListener):
	"""Class that prints out tweets or error assoociated with a tweet"""

	def __init__(self, filename):
		"""Initialise the attribute of the filename which we'll write the streamed tweets to"""
		self.filename = filename

	def on_data(self, data):
		"""Override this method from the parent class to print out the data
		that we get from the StreamListener class and write the printed tweets to self.filename file. 
		"""
		try:
			with open(self.filename, 'a') as file_object:
				file_object.write(data)
			return True
		except BaseException as e:
			pass
		return True


	def on_error(self, status):
		"""Override this method from the parent class to print out the error associated with 
		data/tweet receieved from  StreamListener with an error"""
		print(status) 


if __name__ == '__main__':

	key_words = ['#bitcoin']
	filename = 'cryptocurrency_tweets.json'

	twitter_stream = TwitterStreamer()
	twitter_stream.stream_tweets(filename, key_words)