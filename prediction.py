#!/usr/bin/python2 -tt

import numpy as np
from copy import deepcopy
from graph import graphProp
import shell


def predictRating(G):
	matrix = []
	if not G.nodes():
		return 0
	gp = graphProp(G)
	for movie in gp.getMovies():
		details = gp.getMovieDetails(movie)
		matrix.append([details['year'], details['ratings']])
	matrix.sort()
	matrix = np.array(matrix)
	average = np.average(matrix, axis=0)
	matrix = matrix[np.where(matrix[:, 1] >= average[1])]
	X, Y = matrix[:, 0], matrix[:, 1]
	X = np.append(np.ones((1, X.shape[0])), X[np.newaxis, :], axis=0)
	theta = np.matmul(Y, np.linalg.pinv(X)).transpose()
	rating = np.matmul(theta.transpose(), X)[-1]
	return rating


def associativity(*args):
	if len(args) == 1:
		return 1
	numerator = np.sum(np.product(args, axis=0))
	denominator = np.product(np.linalg.norm(args, axis=1))
	if denominator == 0:
		return 0
	output = float(numerator) / denominator
	return output


def movies_ratings(G, name, role_type):
	if name not in G.nodes():
		query = "SUGGEST '{}'".format(name)
		result = shell.process_query(G, query)
		new_name = result.edges()[0][1]
		print "*** Using {} instead of {} ***".format(new_name, name)
		name = new_name
	query = "GET year, ratings OF * WITH {} AS ['{}']".format(role_type, name)
	result = shell.process_query(G, query)
	gp = graphProp(result)
	return gp.getMovies(), result


def getWeightedRating(assoc_rat):
	numerator = 0
	denominator = 0
	for key in assoc_rat:
		numerator += assoc_rat[key]['rating'] * assoc_rat[key]['assoc']
		denominator += assoc_rat[key]['assoc']
	return float(numerator) / denominator


def getCombinationSet(items):
	output = []
	if len(items) <= 1:
		return [items[:]]
	for i in xrange(0, len(items)):
		combSet = getCombinationSet(items[i+1:])
		output.extend(deepcopy(combSet))
		for j in xrange(0, len(combSet)):
			combSet[j].append(items[i])
		output.extend(combSet)
		output.append([items[i]])
	return output


def predict(G, args, flag):
	roles = args['actors'][:]
	roles.extend(args['directors'])
	roles.extend(args['genres'])
	details_list = []
	tot_movies = set()

	for name in args['actors']:
		movies, ratings_G = movies_ratings(G, name, 'actors')
		details_list.append({'movies': movies, 'graph': ratings_G})
		tot_movies.update(movies)

	for name in args['directors']:
		movies, ratings_G = movies_ratings(G, name, 'directors')
		details_list.append({'movies': movies, 'graph': ratings_G})
		tot_movies.update(movies)

	for name in args['genres']:
		movies, ratings_G = movies_ratings(G, name, 'genres')
		details_list.append({'movies': movies, 'graph': ratings_G})
		tot_movies.update(movies)

	tot_movies = list(tot_movies)

	for i in xrange(len(details_list)):
		vector = np.zeros(len(tot_movies))
		for movie in details_list[i]['movies']:
			index = tot_movies.index(movie)
			vector[index] = 1
		details_list[i]['vector'] = vector

	assoc_rat_dict = dict()
	combinations = list({tuple(t) for t in getCombinationSet(range(len(roles))) if t})
	for combination in combinations:
		# Calculate association
		vectors = [details_list[ind]['vector'] for ind in combination]
		num_perm = np.product(range(1, len(combination)+1))
		assoc = associativity(*vectors) * num_perm

		ind = combination[0]
		g1 = details_list[ind]['graph']
		if len(combination) > 1:
			for j in combination[1:]:
				gp = graphProp(g1)
				g1 = gp.edgeIntersection(details_list[j]['graph'])
		rating = predictRating(g1)
		assoc_rat_dict[combination] = {'assoc': assoc, 'rating': rating}

	if flag:
		print dict(enumerate(roles))
		print assoc_rat_dict
	output = getWeightedRating(assoc_rat_dict)
	return output


def start(G, flag=False):
	print "Multiple values to be seperated by ,"

	actors = raw_input('Input actors: ')
	actors = map(str.strip, actors.split(','))

	directors = raw_input('Input directors: ')
	directors = map(str.strip, directors.split(','))

	genres = raw_input('Input genres: ')
	genres = map(str.strip, genres.split(','))

	args = {'actors': actors, 'directors': directors, 'genres': genres}
	return predict(G, args, flag)

if __name__ == '__main__':
	import pickle
	G = pickle.load(open(r'data/hollygraph.pkl', 'rb'))
	start(G)

