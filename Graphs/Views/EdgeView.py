"""
This class is the view for edges
"""

import tkinter

class EdgeView():

	def __init__(self, canvas, v1, v2 = None, label = "edge", weight = 0, edgeID = "edge"):
		self.canvas = canvas
		self.v1 = v1
		self.v2 = v2
		self.fillColor = "red"
		if v2 is None:
			self.fillColor = "black"
			self.v2 = v1
		self.line = self.canvas.create_line(
			self.v1.x, self.v1.y,
			self.v2.x, self.v2.y,
			fill=self.fillColor)
		self.deleted = False
		self.weight = weight
		self.label = canvas.create_text(
			(self.v1.x + self.v2.x) / 2,
			(self.v1.y + self.v2.y) / 2 - 10,
			text = label + ": " + str(weight))
		self.labelText = label
		self.edgeID = edgeID



	def delete(self):
		self.canvas.delete(self.line)
		self.canvas.delete(self.label)
		self.line = None
		self.deleted = True

	def followMouseEvent(self, event):
		self.x = event.x
		self.y = event.y
		self.fillColor = "black"

		self.redraw()

	def updateWeight(self, weight):
		self.weight = weight
		self.redraw()

	def redraw(self):
		if self.deleted:
			return
		self.canvas.delete(self.line)
		self.canvas.delete(self.label)
		x1 = self.v1.x
		y1 = self.v1.y
		x2 = None
		y2 = None
		if self.v2 == self.v1:
			x2 = self.x
			y2 = self.y
		else:
			x2 = self.v2.x
			y2 = self.v2.y

		self.line = self.canvas.create_line(
			x1, y1, x2, y2,
			fill=self.fillColor, width = 3)

		self.label = self.canvas.create_text(
			(x1 + x2) / 2,
			(y1 + y2) / 2 - 10,
			text = self.labelText + ": " + str(self.weight))
