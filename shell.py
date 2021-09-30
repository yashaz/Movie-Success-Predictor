#!/usr/bin/python2 -tt


from __future__ import print_function
from graph import graphProp


def process_query(graph, query):
	if query.startswith('GET'):
		import query_get as getQ
		return getQ.process(graph, query)

	elif query.startswith('SUGGEST'):
		import query_suggest as sugQ
		return sugQ.process(graph, query)

	else:
		raise ValueError("Incorrect query")


def start(graph):
	print("-------------------------")
	print("    Welcome to Shell     ")
	print("-------------------------")
	while True:
		try:
			query = raw_input("<<< ").strip()
		except EOFError:
			print("\nQuitting")
			break
		if not query:
			continue
		if query.lower() == "quit":
			break
		try:
			result = process_query(graph, query)
			display(result)
		except ValueError as ve:
			print(ve)


def display(graph, flag=False):
	output = []
	gp = graphProp(graph)
	for disGraph in gp.getDisconnectedGraphs():
		init_node = disGraph.nodes()[0]
		is_movie = gp.is_movie(init_node)
		if not is_movie[0]:
			init_node = is_movie[1][0]
		movies = set()
		movies.add(init_node)
		visited = set()
		while movies:
			movie = movies.pop()
			visited.add(movie)
			for edge in disGraph.out_edges(movie, data=True):
				output.append((movie, edge[2]['type'], edge[1]))
				for mov in disGraph.in_edges(edge[1]):
					if mov[0] not in visited:
						movies.add(mov[0])
			disGraph.remove_node(movie)
	if flag:
		return output

	for movie in sorted(output):
		text = u"{} --{}--> {}".format(*movie)
		print(text)
	print("Total Results:", len(output))

if __name__ == '__main__':
	import pickle
	G = pickle.load(open('data/hollygraph.pkl'))
	start(G)