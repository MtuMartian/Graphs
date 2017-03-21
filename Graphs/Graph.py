"""
This is the implementation of the graph class
"""

from NodeData import Edge
from NodeData import Vertex

class Graph:

	def __init__(self, name = "G"):
		self.vertices = []
		self.edges = []
		self.name = name

	def addVertex(self, vertex):
		self.vertices.append(vertex)

	def addEdge(self, vertex1, vertex2, uuid, name = "", weight = 1):
		#TODO: Validate vertices
		edge = Edge(vertex1, vertex2, uuid, name, weight)
		vertex1.addEdge(edge)
		vertex2.addEdge(edge)
		self.edges.append(edge)

	def removeEdge(self, vertex1, vertex2):
		rEdge = None
		for edge in self.edges:
			if edge.checkEquality(vertex1, vertex2):
				self.edges.remove(edge)
				rEdge = edge
		if rEdge is None:
			return
		vertex1.removeEdge(rEdge)
		vertex2.removeEdge(rEdge)

	def getVertexById(self, vid):
		for vertex in self.vertices:
			if vertex.id == vid:
				return vertex

	def getEdgeByVertIds(self, vid1, vid2):
		vert1 = self.getVertexById(vid1)
		vert2 = self.getVertexById(vid2)
		for edge in vert1.edges:
			if edge in vert2.edges:
				return edge

	def removeEdgeByVertIds(self, vid1, vid2):
		vert1 = self.getVertexById(vid1)
		vert2 = self.getVertexById(vid2)
		self.removeEdge(vert1, vert2)

	def printVertices(self):
		print("Graph " + self.name + " has vertices:")
		for vertex in self.vertices:
			vertex.printName()

	def printVerticesFormatted(self):
		print("Graph " + self.name + " has vertices:")
		for vertex in self.vertices:
			vertex.printDataFormatted()

	def printEdgesFormatted(self):
		print("Graph " + self.name + " has edges:")
		for edge in self.edges:
			edge.printDataFormatted()

	def printInfo(self):
		self.printVerticesFormatted()
		self.printEdgesFormatted()
