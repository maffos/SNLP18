from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os

import json
import applicationData


#This class obtains tweets from twitter
class TwitterStreamer():
    def __init__(self):
        pass

    def stream_tweets(self, filename, min_tweet_size, max_tweets, keywords):
        listener = MyListener(filename, min_tweet_size, max_tweets)
	
	# Authentication for the Twitter Streaming API        
	auth = OAuthHandler(applicationData.CONSUMER_KEY, applicationData.CONSUMER_SECRET)
        auth.set_access_token(applicationData.ACCESS_TOKEN, applicationData.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # Only collect tweets that are in hindi
        stream.filter(track = keywords, languages=["hi"])


# # # # TWITTER STREAM LISTENER # # # #
class MyListener(StreamListener):
    #tweets are printed to stdout and saved to a .json file
    
    def __init__(self, filename, min_tweet_size, max_tweets):
        self.filename = filename
        
        #if the stream ran previously but not all of the tweets have been collected, yet, don't start counting from zero
	with open('/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/tweet_count.txt') as f:
		first_line = f.readline().strip()
	self.tweet_counter = int(first_line)
        print("Amount of tweets fetched so far: " + str(self.tweet_counter))
        self.min_tweet_size = min_tweet_size
	self.max_tweets = max_tweets

    def on_data(self, data):
        try:
	    #create a temporary file to count the size of the tweet
	    with open('/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/temp.json', 'w+') as temp:
		temp.write(data)		
	    with open('/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/temp.json', 'r') as temp:		
		temp_data = json.load(temp)
		tweet_size = len(temp_data["text"])
	    os.remove('/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/temp.json')
	    
	    #only tweets with a size equal or higher than 50 are processed, stops when max amount of tweets is reached
	    if tweet_size >= self.min_tweet_size and self.tweet_counter < self.max_tweets:
		#increments the counter for tweets
	    	self.tweet_counter += 1
            	with open('/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/tweet_count.txt', 'w') as f:
			f.seek(0)
			f.truncate()
			f.write(str(self.tweet_counter))            
	    	#the tweet is printed to stdout
	    	print(data)
            
	    	#append the tweet to hin.json
		with open(self.filename, 'a') as file:
			file.write(data)
			#append a comma, for the next object
			if self.tweet_counter < self.max_tweets:
				file.write(", \n")
	    elif self.tweet_counter == max_tweets:
		return False
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True
          

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    #list of hindi seed words, translated into latin alphabet. Translation from: http://mylanguages.org/hindi_romanization.php
    keywords = ["smbndh", "nhin", "gayaa", "apne", "thata", "sath", "nahi", "chalo", "madharchod", "hai", "hain"]

    #Path to the json file were the tweets are being safed 
    filename = "/home/matthias/Schreibtisch/Uni/6.Semester/SNLP/Assignments/Assignment_1/hin.json"
    with open(filename, 'w') as f:
	f.write("[ \n")
    max_tweets = 10000
    min_tweet_size = 50
    #instantiates an Object of the Class TwitterStreamer
    twitter_streamer = TwitterStreamer()
twitter_streamer.stream_tweets(filename, min_tweet_size, max_tweets, keywords)

#close the Json Array
with open(filename, 'a') as f:
	f.write("]")
