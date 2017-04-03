"""
This is the main view
"""

import tkinter
import MouseReader

def main():
	mainWindow = tkinter.Tk()

	# Create a canvas to display the graph
	canvas = tkinter.Canvas(mainWindow, width = 1200, height = 600)
	canvas.pack()
	# Create border
	canvas.create_line(10, 10, 10, 590)
	canvas.create_line(10, 10, 1190, 10)
	canvas.create_line(1190, 10, 1190, 590)
	canvas.create_line(10, 590, 1190, 590)
	# Create a canvas for the menu
	menuCanvas = tkinter.Canvas(mainWindow, width = 1200, height = 100)
	menuCanvas.pack()
	# Create an entry for user to input commands
	commandEntry = tkinter.Entry()
	commandEntry.pack()

	# Create a mouse reader object to read mouse input
	mouseInput = MouseReader.MouseReader(canvas, menuCanvas, commandEntry)
	entryButton = tkinter.Button(mainWindow, text="Submit Command", command = mouseInput.receiveCommand)
	entryButton.pack()
	# Bind the mouse reader to the canvases
	canvas.bind("<Button-1>", mouseInput.mainCanvasClickedEvent)
	canvas.bind("<Motion>", mouseInput.mainCanvasMouseOverEvent)
	canvas.bind("<ButtonRelease-1>", mouseInput.mainCanvasMouseUpEvent)

	# Bind the enter button to submitting a command
	mainWindow.bind('<Return>', mouseInput.receiveCommand)

	mainWindow.mainloop()

if __name__ == "__main__":
	main()
