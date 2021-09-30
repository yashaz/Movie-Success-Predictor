#!/usr/bin/python2 -tt

from sys import argv
import pickle
import twittersentiment as ts
import prediction as predict
import shell


def main():
	if len(argv) > 1:
		if argv[1] == "twitter":
			if len(argv) < 3:
				print "Enter name"
			else:
				name = argv[2]
				limit = 100
				if len(argv) == 4:
					limit = int(argv[3].strip())
				data = ts.twitters(name, limit)
				probs = ts.probability(data)
				print "Twitter Probability {}".format(probs)
		G = pickle.load(open('data/hollygraph.pkl'))
		print "Graph Loaded"
		if argv[1] == "shell":
			shell.start(G)
		if argv[1] == "predict":
			flag = False
			if argv[-1].lower() == "true":
				flag = True
			rating = predict.start(G, flag)
			print "Predicted Rating: {}".format(rating)
			if argv[-1] == "true":
				return
			if len(argv) >= 3:
				print "Analysing twitter"
				if not argv[2] == "twitter":
					print "Invalid flag"
					return
				name = argv[3]
				limit = 100
				if len(argv) == 5:
					limit = int(argv[4].strip())
				data = ts.twitters(name, limit)
				probs = ts.probability(data)
				print "Final Rating with Twitter: {}".format(rating + probs[2] - probs[0])
	else:
		print "Enter Flags"

if __name__ == '__main__':
	main()