#!/usr/bin/python2 -tt

import json
import networkx as nx
import pickle


def process(fileName, outFile):
	dataset = json.load(open(fileName, 'rb'))
	G = nx.DiGraph()
	for movie in dataset:
		if movie['movie'] in G.nodes():
			continue
		if not movie['ratings'] or not movie['year']:
			continue
		for actor in movie['actors']:
			G.add_edge(movie['movie'], actor, {'type': 'actor'})
		for director in movie['directors']:
			G.add_edge(movie['movie'], director	, {'type': 'director'})
		for genre in movie['genres']:
			G.add_edge(movie['movie'], genre, {'type': 'genre'})
		G.add_edge(movie['movie'], movie['ratings'], {'type': 'rating'})
		G.add_edge(movie['movie'], movie['year'], {'type': 'year'})
	pickle.dump(G, open(outFile, 'wb'))


if __name__ == '__main__':
	process('data/bollydataset.json', 'data/bollygraph.pkl')
