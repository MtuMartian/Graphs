"""
This is the testing file
"""
import NodeData
import Graph

def main():
	v1 = NodeData.Vertex("v1")
	v2 = NodeData.Vertex("v2")
	v3 = NodeData.Vertex("v3")
	g = Graph.Graph("G")
	g.addVertex(v1)
	g.addVertex(v2)
	g.addVertex(v3)
	g.addEdge(v1, v2)
	g.addEdge(v3, v2)
	g.printVerticesFormatted()
	g.removeEdge(v2, v1)
	g.printVerticesFormatted()

if __name__ == "__main__":
	main()