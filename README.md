# Graphs

## Installation and running

* Python 3 is required to run the application. If you do not already have Python 3 installed, download it here: https://www.python.org/downloads/
* Once Python 3 is installed, download this project as a Zip or clone the repository
* To run, using the terminal, cd into the directory containing Main.py and run the command "python3 Main.py"
* A window should appear with a box and a text input element. The application is now running

## Creating graphs

This application allows you to create undirected graphs with weighted edges. To create a vertex, simply left click anywhere within the main box.
All other operations are done using the input element at the bottom of the screen. The format for entering a command is:

> \<commandname\>:\<arg1\>:\<arg2\>: ... :\<argn\>

After typing your command, press the enter button to run it. Note that if the command takes no args, then a colon is not necessary and will potentially cause an error.
The list of commands and their arguments are:

* addEdge args: vertex1, vertex2
  Adds an edge between two vertices
  vertex1 and vertex2 are the labels of the vertices which you want to add the edge between
Example:
> addEdge:v0:v3
* removeEdge args: vertex1, vertex2
  Removes an edge between two vertices if the edge exists
  vertex1 and vertex2 are the labels of the vertices which you want to remove the edge from
Example: 
> removeEdge:v2:v3
* removeVertex args: vertex
  Removes a vertex and all incident edges
  vertex is the label of teh vertex to be removed
Example: 
> removeVertex:v0
* updateEdgeWeight args: vertex1, vertex2, weight
  Changes the weight of edge between two vertices
  vertex1 and vertex2 are the labels of the vertices that the edge is between
  weight is the new weight for the edge  
Example: 
> updateEdgeWeight:v0:v1:17
* printGraphInfo (no args)
  Prints info about the vertices and edges of the graph in the console
Example: 
> printGraphInfo
* bipartite (no args)
  Creates a bipartition in the graph if the graph is bipartite.
  After creating the bipartition, all vertices will be colored either yellow or purple.
  However, you will need to mouse over the vertices for the color change to take effect.
Example: 
> bipartite
* dijkstra args: originVertex
  Performs Dijkstra's Algorithm on the graph with a given origin. After
  performing the algorithm, all edges of the shortest paths will be colored purple, however, you will
  have to move your mouse over all vertices for the color change to take effect.
Example: 
> dijkstra:v0

**WARNING! KNOWN ISSUE:** Performing Dijkstra's algorithm a second time will not clear the coloring put in place by the previous algorithm
Also, sometimes performing Dijkstra's algorithm a second time will cause an error. I believe this is because of a pass by reference
instead of value issue but have not tested it extensively yet

## Implementation
Implementation is fairly straight forward and will be split into three parts

### Graph
The graph itself is defined in the files Graph.py and NodeData.py
NodeData.py contains class definitions for vertices and edges
Graph.py contains the class definition for the graph itself as well as algorithms to perform on the graph.
Graph.py also contains a modified heap sort that sorts vertices by their "distance" for Dijkstra

### Input Handler
The MouseReader.py contains a class that handles all user input and keeps a collection of id's that refer to vertices and edges.
These ids are mapped to the views and each vertex and edge with the graph also contains a copy of the id. This is so that connecting the
graph to the view of the graph can be done easily without extensive searching.

### Views
The view files control what is shown to the user in the user interface. There are two files: Views/EdgeView.py and Views/VertexView.py
EdgeView.py contains a class definition that draws an edge between two vertex views
VertexView.py contains a class definition that draws circles to represent vertices

