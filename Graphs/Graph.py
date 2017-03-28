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

	def getEdgeById(self, eid):
		for edge in self.edges:
			if edge.id == eid:
				return edge

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

	# *** ALGORITHMS *** #

	"""
	If G is a bipartite graph, this function finds a bipartition and returns the two sets of vertices
	If G is not a bipartite graph, returns None
	"""
	def createBipartition(self):
		# Check if the graph is empty
		if len(self.vertices) == 0:
			return None
		# Create a 'queue' that stores vertices to be checked
		queue = []
		# Add an arbitrary vertex to the queue. Note: For simplicity I add the first vertex in the vertex
		# list. However, the algorithm will work regardless of what vertex you start with
		queue.append(self.vertices[0])
		# Partition the first vertex to partition 0
		queue[0].partition = 0
		# Loop until all vertices have been visited (This loop is repeated |V| times)
		while len(queue) > 0:
			# Get the next vertex from the queue
			vertex = queue[0]
			# Go to each adjacent vertex (This loop is repeated |adj(vi)| times)
			for adj in vertex.adjacentVertices():
				# If the adjacent vertex is not partitioned, partition it to the set opposite the
				# current vertex then add to the queue so its adjacent vertices will be checked later
				if adj.partition is None:
					adj.partition = (vertex.partition + 1) % 2
					queue.append(adj)
				# If the adjacent vertex has been partitioned and is in the same set as the current
				# vertex, then the graph cannot be bipartite
				if adj.partition == vertex.partition:
					print("Bipartition does not exist")
					return None
			# Remove the current vertex from the queue
			queue.remove(vertex)
		# Get a list of the vertices for each partition
		part1 = [vertex for vertex in self.vertices if vertex.partition == 0]
		part2 = [vertex for vertex in self.vertices if vertex.partition == 1]
		# Return a map of the two sets of vertices
		return {'part1' : part1, 'part2' : part2}

	"""
	
	"""
	def dijkstra(self, start):
		# Create map for previous vertices
		previous = {}
		# Reset vertex distances and previouses
		for vertex in self.vertices:
			vertex.distance = 9999
			previous[vertex.id] = None
		# Origin distance is 0
		start.distance = 0
		# Create copy of vertices in graph
		allVertices = self.vertices
		# Heapsort the vertices
		heapsort(allVertices)
		# Loop for each vertex
		while len(allVertices) > 0:
			# Get the vertex with lowest weight
			current = allVertices[0]
			# Remove that vertex from the temporary list
			allVertices.remove(current)
			# For all adjacent vertices check to see if taking the current vertex reduces travel time
			for neighbor in current.adjacentVertices():
				alternativeDistance = current.distance + neighbor.connectingEdge(current).weight
				if alternativeDistance < neighbor.distance:
					previous[neighbor.id] = current.id
					neighbor.distance = alternativeDistance
			# Heapsort all vertices again
			heapsort(allVertices)

		return previous


def heapsort( lst ):
  length = len( lst ) - 1
  leastParent = int(length / 2)
  for i in range ( leastParent, -1, -1 ):
    moveDown( lst, i, length )
 
  # flatten heap
  for i in range ( length, 0, -1 ):
    if lst[0].distance > lst[i].distance:
      swap( lst, 0, i )
      moveDown( lst, 0, i - 1 )
 
 
def moveDown( lst, first, last ):
  largest = 2 * first + 1
  while largest <= last:
    # right child exists and is larger than left child
    if ( largest < last ) and ( lst[largest].distance < lst[largest + 1].distance ):
      largest += 1
 
    # right child is larger than parent
    if lst[largest].distance > lst[first].distance:
      swap( lst, largest, first )
      # move down to largest child
      first = largest;
      largest = 2 * first + 1
    else:
      return # force exit
 
 
def swap( A, x, y ):
  tmp = A[x]
  A[x] = A[y]
  A[y] = tmp














