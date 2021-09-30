from __future__ import print_function
import tweepy
import sys
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def twitters(search, no=100):
	tot_keys = [
		{
			'ckey': 'Consumer Key',
			'csecret': 'Consumer Secret',
			'atoken': 'Access Token',
			'asecret': 'Access Secret'
		}
	]

	for keys in tot_keys:
		ckey = keys['ckey']
		csecret = keys['csecret']
		atoken = keys['atoken']
		asecret = keys['asecret']
		auth = tweepy.OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)

		api = tweepy.API(auth)
		q = search
		texts = set()
		limit = no
		cursor = tweepy.Cursor(api.search, q=q, lang='en').items()
		output = []
		try:
			while len(texts) < limit:
				try:
					tweet = next(cursor)
				except StopIteration:
					print("")
					return output
				if tweet.text.find('https:') >= 0:
					continue
					
				sid = SentimentIntensityAnalyzer()
				sentence=tweet.text.encode('utf8')
				texts.add(sentence)
				#print(sentence)
				ss = sid.polarity_scores(sentence)
				output.append([ss['neg'], ss['neu'], ss['pos']])
				sys.stdout.flush()
				sys.stdout.write("\rTexts collected {}".format(len(texts)))
			print("")
			return output
		except tweepy.error.TweepError:
			continue


def probability(array):
	array = np.array(array)
	average = np.average(array, axis=0)
	return average

if __name__ == '__main__':
	print(twitters(sys.argv[1]))