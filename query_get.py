#!/usr/bin/python2 -tt

import re
from graph import graphProp


def get_func(graph, param):
	if param.strip() == "*":
		return graph
	nodes = map(str.strip, eval("['" + param.replace(",", "','") + "']"))
	gp = graphProp(graph)
	output = gp.emptyGraph()
	for edge in graph.edges(data=True):
		if edge[-1]['type'] + "s" in nodes or edge[-1]['type'] in nodes:
			output.add_edge(*edge)
	return output


def of_func(graph, param):
	gp = graphProp(graph)
	if param.strip() == "*":
		return graph
	else:
		param = eval(param)
		if isinstance(param, str) or isinstance(param, unicode):
			nodes = [param]
		else:
			nodes = list(param)
	# return nodes
	try:
		output = gp.getGraphFrom(nodes.pop())
	except IndexError:
		return gp.emptyGraph()
	for node in nodes:
		output.add_edges_from(gp.getGraphFrom(node).edges(data=True))
	return output


def with_func(graph, main_param):
	gp = graphProp(graph)
	output = gp.emptyGraph()
	pattern = re.compile(r'(\S+)\s+AS\s+(\[[^AS]*\])')
	main_param = main_param.replace('(', '( ').replace(')', ' )')
	for movie in gp.getMovies():
		movie_details = gp.getMovieDetails(movie)
		ratings = movie_details['ratings']
		year = movie_details['year']
		param = main_param
		if "AS" in main_param:
			splits = pattern.split(main_param)
			final_splits = []
			for i in range(1, len(splits), 3):
				final_splits.append(splits[i-1])
				user_choices = set(eval(splits[i+1]))
				movie_choices = set(movie_details[splits[i]])
				inter_choices = user_choices.intersection(movie_choices)
				final_splits.append(str(inter_choices == user_choices))
			final_splits.extend(splits[i+2:])
			param = ' '.join(final_splits)
		param = param.replace('AND', 'and').replace('OR', 'or')
		condition = eval(param)
		if condition:
			output.add_edges_from(graph.edges(movie, data=True))
	return output


def process(graph, query):
	func_dict = {'get': get_func, 'of': of_func, 'with': with_func}
	params = query.split('GET')
	temp = params.pop(-1)
	params.extend(temp.split('OF'))
	temp = params.pop(-1)
	params.extend(temp.split('WITH'))
	params = map(str.strip, params)
	input_graph = graph
	if len(params) > 2:
		input_graph = func_dict['of'](input_graph, params[2])
	if len(params) > 3:
		input_graph = func_dict['with'](input_graph, params[3])
	# print(input_graph.edges(data=True))
	input_graph = func_dict['get'](input_graph, params[1])
	return input_graph
