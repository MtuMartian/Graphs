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
from enum import Enum
from uuid import uuid4

class MouseReader():

	def __init__(self, canvas, menuCanvas, commandEntry):
		self.strToFunc = {"restart" : self.restart, 
			"removeEdge" : self.removeEdgeByID,
			"removeVertex" : self.removeVertexByID,
			"updateEdgeWeight" : self.updateWeight}

		# Define initial state
		self.state = State.NONE
		# Declare graph data object
		self.graph = Graph()
		# Initialize lists to store vertices and edges
		self.vertices = []
		self.edges = []
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
		# Parameters for menu icons
		self.menuOvalX = 100
		self.menuOvalY = 50
		self.menuOvalSize = 50

		self.menuLineX = 200
		self.menuLineY = 50
		self.menuLineSize = 50
		# Draw menu icons
		self.menuCanvas.create_oval(
			self.menuOvalX - self.menuOvalSize / 2,
			self.menuOvalY - self.menuOvalSize / 2,
			self.menuOvalX + self.menuOvalSize / 2,
			self.menuOvalY + self.menuOvalSize / 2, fill="blue")
		self.menuCanvas.create_line(
			self.menuLineX - self.menuLineSize / 2,
			self.menuLineY - self.menuLineSize / 2,
			self.menuLineX + self.menuLineSize / 2,
			self.menuLineY + self.menuLineSize / 2)
		

	"""
	Event called when the main canvas is clicked. Depending on the state
	the event may trigger:
		a vertex being placed
		an edge being placed
		a vertex being moved
	"""
	def mainCanvasClickedEvent(self, event):
		if self.state == State.PLACING_VERTEX:
			self.placeVertex(event)
		if self.state == State.PLACING_EDGE:
			self.placeEdge(event)
		if self.state == State.NONE:
			self.moveVertex(event)

	"""
	When the mouse is lifted, the dragging vertex should
	be set to none
	"""
	def mainCanvasMouseUpEvent(self, event):
		self.draggingVertex = None

	"""
	Changes state depending on where on the menu was clicked
	"""
	def menuCanvasClickedEvent(self, event):
		x = event.x
		y = event.y
		if (x >= self.menuOvalX - self.menuOvalSize / 2) and (x <= self.menuOvalX + self.menuOvalSize / 2):
			self.setState(State.PLACING_VERTEX)
		elif (x >= self.menuLineX - self.menuLineSize / 2) and (x <= self.menuLineX + self.menuLineSize / 2):
			self.setState(State.PLACING_EDGE)
		else:
			self.setState(State.NONE)

	"""
	Highlights any vertices under the mouse.
	If currently moving a vertex, calles the move method of the vertex
	If currently placing an edge, creates an edge that will follow the mouse
    """
	def mainCanvasMouseOverEvent(self, event):
		for vertex in self.vertices:
			if vertex.deleted:
				self.vertices.remove(vertex)
			elif vertex.containsPoint(event.x, event.y):
				vertex.mouseEnterEvent(event)
			elif not vertex.containsPoint(event.x, event.y):
				vertex.mouseExitEvent(event)

		if self.draggingVertex is not None:
			self.draggingVertex.move(event)

		if self.state == State.PLACING_EDGE and not self.selectedVertex is None:
			if self.placingEdge is None:
				self.placingEdge = EdgeView(self.canvas, self.selectedVertex)
			self.placingEdge.followMouseEvent(event)

	"""
	Deletes any left over vertices then places a vertex at the
	given point unless there is already one in that location
	"""
	def placeVertex(self, event):
		for vertex in self.vertices:
			if vertex.deleted:
				self.vertices.remove(vertex)
			elif vertex.containsPoint(event.x, event.y):
				vertex.clickedEvent(event)
				print(self.graph.printVerticesFormatted())
				return

		vID = self.vIDGen.genNew()
		vLabel = "v" + str(vID)
		vertex = VertexView(self.canvas, event.x, event.y, vID, label = vLabel)
		self.vertices.append(vertex)
		self.graph.addVertex(Vertex(vLabel, vID))

	"""
	Create a new edge at the location of the mouse if there is
	a vertex there
	"""
	def placeEdge(self, event):
		for vertex in self.vertices:
			if vertex.containsPoint(event.x, event.y):
				if self.selectedVertex is None:
					self.selectedVertex = vertex
					vertex.toggleFocus(True)
				elif self.selectedVertex == vertex:
					self.selectedVertex = None
					vertex.toggleFocus(False)
					self.placingEdge.delete()
					self.placingEdge = None
				else:
					# Place a new edge between the selected vertex and the vertex under the cursor
					edgeID = vertex.labelText + "-" + self.selectedVertex.labelText
					edge = EdgeView(self.canvas, vertex, self.selectedVertex, label = edgeID, edgeID = edgeID)
					self.edges.append(edge)
					vertex.toggleFocus(False)
					vertex.addEdge(edge)

					v1 = self.getVertexFromView(vertex)
					v2 = self.getVertexFromView(self.selectedVertex)
					self.graph.addEdge(v1, v2)

					self.selectedVertex.toggleFocus(False)
					self.selectedVertex.addEdge(edge)
					self.selectedVertex = None
					self.placingEdge.delete()
					self.placingEdge = None
				return

	"""
	Selects the vertex under the mouse to be the vertex being moved
	"""
	def moveVertex(self, event):
		for vertex in self.vertices:
			if vertex.deleted:
				self.vertices.remove(vertex)
			elif vertex.containsPoint(event.x, event.y):
				self.draggingVertex = vertex

	"""
	Given a vertex view, gives the vertex data associated with it
	"""
	def getVertexFromView(self, view):
		for vertex in self.graph.vertices:
			if vertex.id == view.id:
				return vertex

	def removeVertex(self, vertex):
		vertex.delete()
		self.vertices.remove(vertex)
		# TODO: Automatically remove from the graph as well

	def removeVertexByID(self, *vertexIDs):
		for vertexID in vertexIDs:
			for vertex in self.vertices:
				if str(vertex.id) == vertexID:
					self.removeVertex(vertex)
					break

	def removeEdge(self, edge):
		edge.delete()
		self.edges.remove(edge)
		# TODO: Automatically remove from the graph as well

	def removeEdgeByID(self, *edgeIDs):
		for edgeID in edgeIDs:
			for edge in self.edges:
				if edge.edgeID == edgeID:
					self.removeEdge(edge)
					break

	def updateWeight(self, edgeID, weight):
		for edge in self.edges:
			if edge.edgeID == edgeID:
				edge.updateWeight(weight)
				return

	def restart(self, graph = Graph()):
		numVertices = len(self.vertices)
		numEdges = len(self.edges)
		for num in range(numVertices):
			self.removeVertex(self.vertices[0])
		for num in range(numEdges):
			self.removeEdge(self.edges[0])
		self.graph = graph
		# Restart id generators
		self.vIDGen = UniqueIDGenerator("v")
		self.eIDGen = UniqueIDGenerator("e")

	def receiveCommand(self):
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

	"""
	Set the current state of the mouse reader
	"""
	def setState(self, newState):
		if self.state == newState:
			self.state = State.NONE
		else:
			self.state = newState

class State(Enum):
	NONE = 1
	PLACING_VERTEX = 2
	PLACING_EDGE = 3
	EDIT = 4
