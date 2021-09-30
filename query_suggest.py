#!/usr/bin/python2 -tt

from graph import graphProp
from triegraph import nodeHandler


def suggest_func(graph, params, limit=1):
	nH = nodeHandler(graph.nodes())
	gP = graphProp(graph)
	output = gP.emptyGraph()
	params = eval(params)
	if isinstance(params, str) or isinstance(params, unicode):
		params = [params]
	for param in params:
		suggestions = nH.suggestions(param, limit)
		for sugg in suggestions:
			output.add_edge(param, sugg[-1], {'type': 'suggest'})
	return output


def process(graph, query):
	func_dict = {'suggest': suggest_func}
	params = query.split('SUGGEST')
	temp = params.pop(-1)
	params.extend(temp.split('LIMIT'))
	limit = 1
	if len(params) > 2:
		limit = int(params[-1])
	input_graph = graph
	input_graph = func_dict['suggest'](input_graph, params[1], limit)
	return input_graph
