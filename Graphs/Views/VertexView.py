"""
This is a view for drawing circles
"""

import tkinter
import math

class VertexView:

	def __init__(self, canvas, x, y, uuid, label = "test"):
		self.canvas = canvas
		self.id = uuid
		self.size = 10
		self.circle = self.canvas.create_oval(
			x - self.size, y - self.size,
			x + self.size, y + self.size,
			fill="green")
		self.x = x
		self.y = y
		self.deleted = False
		self.containsMouse = False
		self.isHighlighted = True
		self.isFocused = False
		self.edges = []
		self.labelMargin = 10
		self.label = self.canvas.create_text(self.x, self.y + self.size + self.labelMargin, text = label)
		self.labelText = label

	def clickedEvent(self, event):
		self.toggleHighlight(not self.isHighlighted)

	def mouseEnterEvent(self, event):
		if self.containsMouse:
			return
		self.toggleHighlight(True)
		self.containsMouse = True

	def mouseExitEvent(self, event):
		if not self.containsMouse:
			return
		self.containsMouse = False
		if not self.isFocused:
			self.toggleHighlight(False)

	def containsPoint(self, x, y):
		delx = x - self.x
		dely = y - self.y
		return math.sqrt(delx ** 2 + dely ** 2) <= self.size

	def delete(self):
		self.canvas.delete(self.circle)
		self.circle = None
		self.canvas.delete(self.label)
		self.label = None
		self.deleted = True

	def toggleFocus(self, isFocused):
		if isFocused == self.isFocused:
			return
		if isFocused:
			self.isFocused = True
			self.toggleHighlight(True)
		else:
			self.isFocused = False
			self.toggleHighlight(False)

	def toggleHighlight(self, isHighlighted):
		if isHighlighted == self.isHighlighted:
			return
		self.isHighlighted = isHighlighted
		self.redraw()

	def move(self, event):
		self.x = event.x
		self.y = event.y
		self.redraw()

	def addEdge(self, edge):
		self.edges.append(edge)

	def redraw(self):
		for edge in self.edges:
			edge.redraw()
		color = "blue"
		if self.isHighlighted:
			color = "green"
		self.canvas.delete(self.circle)
		self.canvas.delete(self.label)
		self.circle = self.canvas.create_oval(
			self.x - self.size, self.y - self.size,
			self.x + self.size, self.y + self.size,
			fill=color)
		self.label = self.canvas.create_text(
			self.x,
			self.y + self.size + self.labelMargin,
			text = self.labelText)

