#To run install tweepy libary via the command <pip install tweepy>
import tweepy
import json

def twitterApiAuth():
	consumerApiKey = 'CTz0wD98HC5gXsH9aAryWdXIM'
	consumerSecretKey = 'BTndqodboIzjshMglvyJLCluJn8vKaYY0Zp7nuteUhKAHXm0OP'
	token = '87066477-jRkH2iK2qAJHS7S1COtcdMOUjT6eUeGNVzQH2Wiro'
	secretToken = 'x23v1xkr5nDprPjZ6tp6qRB3Cry6P89XC79u8iSLEeb6x'

	auth = tweepy.OAuthHandler(consumerApiKey, consumerSecretKey)
	auth.set_access_token(token, secretToken)
	api = tweepy.API(auth)
	return api

def createTweetDict(tweetObject):
	
	tweetDict = {
		'id'				: tweetObject.id,
		'created_at'		: tweetObject.created_at.strftime('%m-%d-%Y %H:%M:%S'),
		'text'				: tweetObject.text,
		'user_id'			: tweetObject.user.id,
		'user_name'			: tweetObject.user.id,
		'user_screen_name'	: tweetObject.user.screen_name,
		'user_location'		: tweetObject.user.location,
		'user_description'	: tweetObject.user.description,
		'user_id'			: tweetObject.user.id,
	}
	return tweetDict
	

def getTweets(handle = '', startDate = '', keyword = ''):
	api = twitterApiAuth()
	outputTweets = []
	for tweet in tweepy.Cursor(api.user_timeline,id=handle).items():
		tweetDate = tweet.created_at
		if startDate !='':
			startDateMonth = startDate.split('-')[0]
			startDateDay   = startDate.split('-')[1]
			startDateYear  = startDate.split('-')[2]
			if int(startDateYear) == int(tweetDate.year):
				if int(startDateMonth) == int(tweetDate.month):
					if int(startDateDay) <= int(tweetDate.day): 
						if keyword!='':
							if keyword.lower() in tweet.text.lower():
								outputTweets.append(createTweetDict(tweet))
						else:
							outputTweets.append(createTweetDict(tweet))
				elif int(startDateMonth) < int(tweetDate.month):
					if keyword!='':
						if keyword.lower() in tweet.text.lower():
							outputTweets.append(createTweetDict(tweet))
					else:
						outputTweets.append(createTweetDict(tweet))
			elif int(startDateYear) < int(tweetDate.year):
				if keyword!='':
					if keyword.lower() in tweet.text.lower():
						outputTweets.append(createTweetDict(tweet))
				else:
					outputTweets.append(createTweetDict(tweet))
		else:
			if keyword!='':
				if keyword.lower() in tweet.text.lower():
					outputTweets.append(createTweetDict(tweet))
			else:
				outputTweets.append(createTweetDict(tweet))

	outputJSON = json.dumps(outputTweets)
	return outputJSON

#res = getTweets('@CybriantMSSP','10-1-2018', 'security')
#print(res)