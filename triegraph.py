#!/usr/bin/python2 -tt


class Node:
	def __init__(self, c, cNodes={}, prop=None):
		self.id = c
		self.prop = prop
		self.cNodes = cNodes

	def addCNodes(self, nodes):
		self.cNodes[nodes[0]] = nodes[1]

	def setProp(self, prop):
		self.prop = prop

	def addProp(self, key, value):
		self.prop[key] = value

	def getCNodes(self):
		return self.cNodes

	def getCNode(self, key):
		return self.cNodes[key]

	def hasCNode(self, key):
		return key in self.cNodes

	def getID(self):
		return self.id

	def getProp(self):
		return self.prop

	def removeProp(self, attr):
		if attr in self.prop:
			self.prop.pop(attr)

	# def resetProp(self, attr):
	# 	if attr in self.prop:
	# 		self.prop.pop(attr)
	# 	for n in self.cNodes:
	# 		self.cNodes[n].resetProp(attr)


class nodeHandler:
	def __init__(self, nodes):
		self.count = 0
		self.root = Node(self.count, cNodes={}, prop={'word': ''})
		self.process(nodes)

	def process(self, nodes):
		for node in iter(nodes):
			root = self.root
			if not isinstance(node, str) and not isinstance(node, unicode):
				continue
			for letter in node:
				self.count += 1
				if not root.hasCNode(letter):
					newNode = Node(self.count, cNodes={})
					prop = root.getProp()
					newNode.setProp({'word': prop['word'] + letter})
					root.addCNodes((letter, newNode))
				root = root.getCNode(letter)

	def getNodes(self):
		return self.root

	def display(self):
		nodes = [self.root]
		while nodes:
			node = nodes.pop(0)
			cnodes = node.getCNodes()
			for key, n in cnodes.iteritems():
				print "{} --{}--> {}".format(node.getID(), key, n.getID()).encode('utf8')
			nodes.extend(cnodes.values())

	def getEndNodes(self, root=None):
		if not root:
			root = self.root
		nodes = [root]
		while nodes:
			node = nodes.pop()
			cnodes = node.getCNodes()
			if not cnodes:
				print node.getProp()['word'].encode('utf8')
			nodes.extend(cnodes.values())

	def nodeCount(self):
		count = 1
		nodes = [self.root]
		while nodes:
			node = nodes.pop()
			cnodes = node.getCNodes()
			count += len(cnodes)
			nodes.extend(cnodes.values())
		print count

	def suggestions(self, word, limit=5):
		table = [range(len(word) + 1)]
		nodes = [self.root]
		nodes[0].addProp('table', table)
		output = [(1000, '')]
		while nodes:
			node = nodes.pop()
			nodeProp = node.getProp()
			cNodes = node.getCNodes().copy()
			m = max(output)
			if cNodes:
				for n in cNodes.copy():
					t = lavenshteinDistance(word, cNodes[n].getProp()['word'], nodeProp['table'])
					cNodes[n].addProp('table', t)
					if len(output) >= limit:
						if min(t[-1]) >= m[0]:
							cNodes.pop(n)
							# print c.getProp()['word'].encode('utf8')
				nodes.extend(cNodes.values())
			else:
				t = nodeProp['table']
				if len(output) >= limit:
					if t[-1][-1] < m[0]:
						output.remove(m)
						output.append((t[-1][-1], nodeProp['word']))
				else:
					output.append((t[-1][-1], nodeProp['word']))
		return sorted(output)


def lavenshteinDistance(a, b, table):
	len_a = len(a)
	table = table[:]
	table.append([n + 1 for n in table[-1]])
	for j in xrange(1, len_a + 1):
		subCost = a[j - 1] != b[-1]
		table[-1][j] = min(table[-2][j] + 1, table[-1][j - 1] + 1, table[-2][j - 1] + subCost)
	return table


def main():
	import pickle
	G = pickle.load(open('hollygraph.pkl'))
	print 'Graph Loaded'
	nH = nodeHandler(G.nodes())
	print 'node handler loaded'
	# nH.display()
	print nH.suggestions('jony dep', 3)
	print nH.suggestions('cristoper nolan', 3)
	# root = nH.getNodes()
	# nH.getEndNodes(root.getCNode('j'))

if __name__ == '__main__':
	main()