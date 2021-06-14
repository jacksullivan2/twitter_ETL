from tweepy.streaming import StreamListener 
from tweepy import OAuthHandler 
from tweepy import Stream 
from twitter_credentials import *
import json 
import mysql.connector
from datetime import datetime 
import jack_passwords 


	
db = mysql.connector.connect(
	host='localhost',
	user='root',
	password=jack_passwords.mysql_server_password(),
	database='cryptocurrency')


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
		listener = MyListener(filename)
		twitter_authenticator = Authenticator()
		auth = twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)
		stream.filter(track=key_words)


class MyListener(StreamListener):
	"""Class that prints out tweets or error assoociated with a tweet"""

	def __init__(self, filename):
		"""Initialise the attribute of the filename which we'll write the streamed tweets to"""
		self.filename = filename

	def on_data(self, data):
		"""Override this method from the parent class. This method is called automatically whenever data arrives to the listener.
		You need to return True to keep the stream going. If you return False, it stops the stream.
		Before returning True or False, you can do whatever you want with the data.   
		"""
		with open(self.filename, 'a') as file_object:
				file_object.write(data)
		
		# The API returns each tweet in the form of a JSON string. Use the json.loads() method to convert that string into a python object 
		# which allows us to easily access the data.
		tweet_dict = json.loads(data)

		# If I convert our python object (dictionary) back into a JSON string with the indent= argument, this gives us a readable JSON 
		# string which I can make sense of and easily see what to extract. I've looked through this string and worked out what to extract.
		#print(json.dumps(tweet_dict, indent=2))

		time = datetime.strptime(tweet_dict['created_at'], "%a %b %d %X %z %Y")
		tweet = tweet_dict['text']
		username = tweet_dict['user']['screen_name']
		followers = tweet_dict['user']['followers_count']
		retweets = tweet_dict['retweet_count']
		quotes = tweet_dict['quote_count']
		replies = tweet_dict['reply_count']
		favourites = tweet_dict['favorite_count']

		#print(type(time))
		#print(time)


		#print(username, time, tweet, followers, retweets, favourites, replies, quotes)
		#print()

		# Now I'm going to store the data I've extracted from each tweet into a MySQL database.
		my_cursor = db.cursor()
		query = "INSERT INTO bitcoin_tweets(username, tweet, created_at, followers, favourites, retweets, replies, quotes)"
		query += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		data = (username, tweet, time, followers, favourites, retweets, replies, quotes)
		my_cursor.execute(query, data)
		db.commit()

		return True


	def on_error(self, status):
		"""Override this method from the parent class. Here we listen for status code 420, if you get this status code then you have to close the
		stream because if something is going wrong, the stream will continue to connecting to the Twitter API. If you don't close the stream 
		after an error has occured you could get banned from accessing the API. 
		"""
		if status == 420:
			return False


if __name__ == '__main__':

	key_words = ['#bitcoin']
	filename = 'bitcoin.json'

	twitter_stream = TwitterStreamer()
	twitter_stream.stream_tweets(filename, key_words)


