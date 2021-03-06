"""
This is the python implementation of vertices and edges
"""

class Vertex:

	def __init__(self, name, uuid):
		self.edgeSet = []
		self.name = name
		self.id = uuid
		self.partition = None
		self.distance = -1

	def adjacentVertices(self):
		adjVertices = []
		for edge in self.edgeSet:
			adjVertices.append(edge.opposite(self))
		return adjVertices

	def connectingEdge(self, adjacent):
		for edge in self.edgeSet:
			if edge.vertex1 == adjacent or edge.vertex2 == adjacent:
				return edge

	def degree(self):
		return len(self.edgeSet)

	def addEdge(self, edge):
		self.edgeSet.append(edge)

	def removeEdge(self, edge):
		self.edgeSet.remove(edge)

	def printName(self):
		print(self.name)

	def printDataFormatted(self):
		print("Adjacent vertices to " + self.name + ":")
		if self.degree() <= 0:
			print("This vertex has degree of 0")
			return
		adjVertices = self.adjacentVertices()
		for vertex in adjVertices:
			vertex.printName()


class Edge:

	def __init__(self, vertex1, vertex2, uuid, name = "", weight=1):
		self.vertex1 = vertex1
		self.vertex2 = vertex2
		self.weight = weight
		self.name = name
		self.id = uuid

	def checkEquality(self, vertex1, vertex2):
		if self.vertex1 == vertex1 and self.vertex2 == vertex2:
			return True
		if self.vertex1 == vertex2 and self.vertex2 == vertex1:
			return True
		return False

	def opposite(self, fromVertex):
		if fromVertex == self.vertex1:
			return self.vertex2
		return self.vertex1

	def printDataFormatted(self):
		print("Edge {0} has weight: {1}".format(self.name, str(self.weight)))

class UniqueIDGenerator:

	def __init__(self, prefix = ""):
		self.last = None
		self.prefix = prefix

	def genNew(self):
		if self.last is None:
			self.last = 0
		else:
			self.last += 1
		return self.last


	def delete(self, num):
		nums.remove(num)

	def prefix(self, num):
		return self.prefix + str(num)
