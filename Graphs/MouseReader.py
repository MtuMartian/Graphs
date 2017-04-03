"""
This class reads mouse input and spawns/deletes objects based on it
"""

from Views.VertexView import VertexView
from Views.EdgeView import EdgeView

from NodeData import Vertex
from NodeData import Edge
from NodeData import UniqueIDGenerator
from Graph import Graph

import tkinter
import random
from enum import Enum
from uuid import uuid4

class MouseReader():

	def __init__(self, canvas, menuCanvas, commandEntry):
		self.strToFunc = {
			"addEdge" : self.addEdge,
			"removeEdge" : self.removeEdgeByVertices,
			"removeVertex" : self.removeVertexByName,
			"updateEdgeWeight" : self.updateWeight,
			"printGraphInfo" : self.printGraphInfo,
			"bipartite" : self.createBipartition,
			"dijkstra" : self.dijkstra,
			"readFile" : self.readFile,
			"genRand" : self.randomGraph
		}

		# Declare graph data object
		self.graph = Graph()
		# Initialize sets to store vertex and edge ids
		self.vertices = set([])
		self.edges = set([])
		# Initialize dictionaries to store vertex and edge Views
		self.vertViews = {}
		self.edgeViews = {}
		# Initialize canvas variables
		self.canvas = canvas
		self.menuCanvas = menuCanvas
		self.commandEntry = commandEntry
		# Initialize id generators for vertices and edges
		self.vIDGen = UniqueIDGenerator("v")
		self.eIDGen = UniqueIDGenerator("e")
		# Initialize variables to keep track of special elements
		self.selectedVertex = None
		self.placingEdge = None
		self.draggingVertex = None

	def getVertIdFromName(self, name):
		for key, vertex in self.vertViews.items():
			if vertex.labelText == name:
				return key

	def getVertNameFromId(self, vid):
		return self.vertViews[vid].labelText

	def getEdgeIdByVertIds(self, vid1, vid2):
		if vid1 not in self.vertices or vid2 not in self.vertices:
			return
		v1 = self.vertViews[vid1]
		v2 = self.vertViews[vid2]

		for edge in v1.edges:
			if edge in v2.edges:
				return edge.edgeID

	"""
	Event called when the main canvas is left clicked
	"""
	def mainCanvasClickedEvent(self, event):
		for key, vertex in self.vertViews.items():
			if vertex.containsPoint(event.x, event.y):
				self.moveVertex(vertex)
				return

		self.addVertex(event.x, event.y)

	"""
	When the mouse is lifted, the dragging vertex should
	be set to none
	"""
	def mainCanvasMouseUpEvent(self, event):
		self.draggingVertex = None

	"""
	Highlights any vertices under the mouse.
	If currently moving a vertex, calles the move method of the vertex
	If currently placing an edge, creates an edge that will follow the mouse
    """
	def mainCanvasMouseOverEvent(self, event):
		for vid in self.vertices:
			vertex = self.vertViews[vid]
			if vertex.deleted:
				self.vertices.remove(vid)
				self.vertViews.pop(vid)
			elif vertex.containsPoint(event.x, event.y):
				vertex.mouseEnterEvent(event)
			elif not vertex.containsPoint(event.x, event.y):
				vertex.mouseExitEvent(event)

		if self.draggingVertex is not None:
			self.draggingVertex.move(event)

	"""
	Deletes any left over vertices then places a vertex at the
	given point unless there is already one in that location
	"""
	def addVertex(self, x, y, checkOverlap = True):
		if checkOverlap:
			for key, vertex in self.vertViews.items():
				if vertex.deleted:
					self.vertices.remove(key)
					self.vertViews.remove(key)
				elif vertex.containsPoint(x, y):
					vertex.clickedEvent(x, y)
					return

		vid = str(uuid4())
		self.vertices.add(vid)

		vLabel = "v" + str(self.vIDGen.genNew())
		vertex = VertexView(self.canvas, x, y, vid, label = vLabel)
		self.vertViews[vid] = vertex
		self.graph.addVertex(Vertex(vLabel, vid))
		return vid

	"""
	Create a new edge at the location of the mouse if there is
	a vertex there
	"""
	def addEdge(self, vert1, vert2, weight=1):
		if vert1 == vert2:
			return
		id1 = self.getVertIdFromName(vert1)
		id2 = self.getVertIdFromName(vert2)
		print("TESTING NEW ADD EDGE METHOD")
		print(id1)
		print(id2)
		edgeId = str(uuid4())
		edgeLabel = vert1 + "-" + vert2
		vertex1 = self.vertViews[id1]
		vertex2 = self.vertViews[id2]
		edge = EdgeView(self.canvas, vertex1, vertex2, label = edgeLabel, edgeID = edgeId, weight = weight)
		self.edges.add(edgeId)
		self.edgeViews[edgeId] = edge
		vertex1.addEdge(edge)
		vertex2.addEdge(edge)
		gv1 = self.graph.getVertexById(id1)
		gv2 = self.graph.getVertexById(id2)
		self.graph.addEdge(gv1, gv2, edgeId, edgeLabel, weight)

	"""
	Selects the vertex under the mouse to be the vertex being moved
	"""
	def moveVertex(self, event):
		for vid in self.vertices:
			vertex = self.vertViews[vid]
			if vertex.deleted:
				self.vertices.remove(vid)
				self.vertViews.remove(vid)
			elif vertex.containsPoint(event.x, event.y):
				self.draggingVertex = vertex

	def removeVertexByName(self, *vertexIDs):
		for vertexID in vertexIDs:
			for key, vertex in self.vertViews.items():
				if str(vertex.labelText) == vertexID:
					self.removeConnectedEdges(vertex)
					vertex.delete()
					self.vertices.remove(key)
					self.vertViews.pop(key)
					break

	def removeEdgeByID(self, *edgeIDs):
		for edgeID in edgeIDs:
			edge = self.edgeViews[edgeID]
			self.edges.remove(edgeID)
			self.edgeViews.pop(edgeID)
			edge.delete()

	def removeConnectedEdges(self, vertex):
		for edge in vertex.edges:
			self.removeEdgeByID(edge.edgeID)

	def removeEdgeByVertices(self, vertex1name, vertex2name):
		vid1 = self.getVertIdFromName(vertex1name)
		vid2 = self.getVertIdFromName(vertex2name)

		edgeID = self.getEdgeIdByVertIds(vid1, vid2)
		if edgeID is None:
			return
		edge = self.edgeViews[edgeID]
		edge.delete()
		self.edges.remove(edgeID)
		self.edgeViews.pop(edgeID)
		self.graph.removeEdgeByVertIds(vid1, vid2)

	def updateWeight(self, v1, v2, weight):
		vid1 = self.getVertIdFromName(v1)
		vid2 = self.getVertIdFromName(v2)
		edgeId = self.getEdgeIdByVertIds(vid1, vid2)
		self.edgeViews[edgeId].updateWeight(weight)
		self.graph.getEdgeById(edgeId).weight = int(weight)

	def createBipartition(self):
		partitions = self.graph.createBipartition()

		if partitions is None:
			return

		for vertex in partitions["part1"]:
			vId = vertex.id
			self.vertViews[vId].color = "purple"
		for vertex in partitions["part2"]:
			vId = vertex.id
			self.vertViews[vId].color = "yellow"

	def dijkstra(self, origin):
		vertId = self.getVertIdFromName(origin)
		print("retrieved vertex id : " + vertId)
		originVertex = None
		for vertex in self.graph.vertices:
			if vertex.id == vertId:
				originVertex = vertex
		if originVertex is None:
			print("Could not find origin...")
			return
		paths = self.graph.dijkstra(originVertex)

		for key, value in paths.items():
			if value is not None:
				edgeId = self.getEdgeIdByVertIds(key, value)
				self.edgeViews[edgeId].fillColor = "purple"

	def printGraphInfo(self):
		self.graph.printInfo()

	def randomGraph(self, numVertices, weightMax, edgeChance):
		vertices = []
		for i in range(int(numVertices)):
			vertices.append(self.addVertex(random.randint(10, 1190), random.randint(10, 390), False))

		for i in range(int(numVertices)):
			for j in range(int(numVertices)):
				if i > j and random.randint(0, 100) < int(edgeChance):
					weight = random.randint(1, int(weightMax))
					v1 = self.getVertNameFromId(vertices[i])
					v2 = self.getVertNameFromId(vertices[j])
					self.addEdge(v1, v2, weight)


	def readFile(self, fileName):
		file = open(fileName, "r")
		firstLine = file.readline().split(" ")
		numVertices = firstLine[0]
		numEdges = firstLine[1]
		print("This file defines a graph with {0} vertices and {1} edges".format(numVertices, numEdges))
		vertices = []
		for i in range(int(numVertices)):
			vertexLine = file.readline().split(" ")
			vertices.append(self.addVertex(int(vertexLine[0]), int(vertexLine[1]), False))

		for i in range(int(numEdges)):
			edgeLine = file.readline().split(" ")
			v1 = self.getVertNameFromId(vertices[int(edgeLine[0])])
			v2 = self.getVertNameFromId(vertices[int(edgeLine[1])])
			weight = edgeLine[2]
			self.addEdge(v1, v2, weight)

	def receiveCommand(self, event=None):
		current = self.commandEntry.get()
		print(current)
		funcDict = self.parseCommand(current)
		if "command" in funcDict:
			funcDict["command"](*funcDict["args"])
		#self.restart()
		self.commandEntry.delete(0, len(current))

	def parseCommand(self, strInput):
		command = strInput.split(":")[0]
		args = strInput.split(":")[1:]
		funcDict = {}
		if command in self.strToFunc:
			funcDict["command"] = self.strToFunc[command]
			funcDict["args"] = args

		return funcDict

