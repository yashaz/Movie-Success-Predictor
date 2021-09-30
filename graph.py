#!/usr/bin/python2 -tt

from networkx import DiGraph


class graphProp:
	def __init__(self, G):
		self.G = G

	def getGraphFrom(self, node, levels=1):
		node = unicode(node)
		G = DiGraph()
		G.add_node(node)
		nodes = [(node, 0)]
		while True:
			node, level = nodes.pop(0)
			if level >= levels:
				break
			to_nodes = self.G.out_edges(node)
			G.add_edges_from(self.G.out_edges(node, data=True))
			temp = to_nodes[:]
			to_nodes = self.G.in_edges(node)
			G.add_edges_from(self.G.in_edges(node, data=True))
			temp.extend(to_nodes)
			nodes.extend([(n, level + 1) for n in temp])
		return G

	def is_movie(self, node):
		edges = self.G.neighbors(node)
		if edges:
			return True, [node]
		else:
			movies = [edge[0] for edge in self.G.in_edges(node)]
			return False, movies

	def getMovieDetails(self, movie):
		movie_details = {'actors': [], 'directors': [], 'genres': []}
		for edge in self.G.edges(movie, data=True):
			type_data = edge[-1]['type']
			if type_data == 'rating':
				movie_details['ratings'] = edge[1]
			elif edge[-1]['type'] == 'year':
				movie_details['year'] = edge[1]
			else:
				movie_details[type_data + "s"].append(edge[1])
		return movie_details

	def emptyGraph(self):
		return DiGraph()

	def edgeIntersection(self, G):
		edges = G.edges(data=True)
		output = DiGraph()
		old_edges = self.G.edges(data=True)
		for edge in edges:
			if edge in old_edges:
				output.add_edges_from([edge])
		return output

	def getMovies(self):
		return set(edge[0] for edge in self.G.edges())

	def getDisconnectedGraphs(self):
		outputG = self.G.copy()
		output = []
		while outputG.nodes():
			output.append(DiGraph())
			start_node = outputG.nodes()[0]
			visited = set()
			nodes = [start_node]
			while nodes:
				node = nodes.pop()
				if node in visited:
					continue
				neighbors = outputG.neighbors(node)
				output[-1].add_edges_from(outputG.out_edges(node, data=True))
				in_edges = outputG.in_edges(node, data=True)
				output[-1].add_edges_from(in_edges)
				for in_edge in in_edges:
					neighbors.append(in_edge[0])
				nodes.extend(neighbors)
				outputG.remove_node(node)
				visited.add(node)
		return output
	

if __name__ == '__main__':
	import pickle
	G = pickle.load(open('hollygraph.pkl'))
	print 'Graph Loaded'
	graph = graphProp(G)
	sG = graph.getGraphFrom('christopher nolan', 1)
	print sG.nodes()