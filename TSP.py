from dataclasses import field
import numpy as np
from collections import defaultdict

CSVData = open("matrix.csv")
TSPcostMatrix = np.loadtxt(CSVData, delimiter=" ")

#This class represents a graph
# using adjacency list representation
class Graph:

	def __init__(self, myCostMatrix,s):
		# No. of vertices
		self.V = len(myCostMatrix)
		self.costMatrix = myCostMatrix
		# default dictionary to store graph
		self.graph = defaultdict(list)
		self.circuits = list(list())
		self.hamiltonianCircuits = list(list())
		self.addEdge()
		self.lowestCost = 0
		self.source = s
		self.sourceVisited = False

	# function to add edges to a graph
	def addEdge(self):
		for i in range(0, self.V):
			for j in range(0, self.V):
				if self.costMatrix[i][j] != -1 :
					self.graph[i].append(j)
				

	#function to find the lowest Cost to travel from source to destination and
	#getting the lowest cost circuit
	def lowestCostcircuit(self):
		indexOfLowestCostcircuits = []
		self.lowestCost = 0
		index = 0
		for hamiltonianCircuit in self.hamiltonianCircuits:
			i = 0
			current = hamiltonianCircuit[i]
			next = hamiltonianCircuit[i+1]
			totalcost = 0
			firstVisit = True
			while current != hamiltonianCircuit[-1] or firstVisit:
				totalcost += self.costMatrix[current][next]
				i+=1
				current = hamiltonianCircuit[i]
				if current != hamiltonianCircuit[-1] or firstVisit:
					next = hamiltonianCircuit[i+1]
				firstVisit = False
			if index == 0:
				self.lowestCost = totalcost
			if totalcost < self.lowestCost:
				self.lowestCost = totalcost
				indexOfLowestCostcircuits.clear()
				indexOfLowestCostcircuits.append(index)
			elif totalcost == self.lowestCost:
				indexOfLowestCostcircuits.append(index)
			index += 1
		return indexOfLowestCostcircuits


	def getAllHamiltonianCircuits(self): 
		for circuit in self.circuits:
			isCircuit = False
			for node in range(0,len(self.circuits)):
				if node not in circuit:
					break
				if node == len(self.costMatrix)-1:
					isCircuit = True
			if isCircuit:
				self.hamiltonianCircuits.append(circuit)

	'''A recursive function to print all circuits from 'u' to 'd'.
	visited[] keeps track of vertices in current circuit.
	circuit[] stores actual vertices and circuit_index is current
	index in circuit[]'''
	def getAllCircuitsUtil(self, u, visited, circuit):
		# Mark the current node as visited and store in circuit
		visited[u]= True
		circuit.append(u)
		# If current vertex is same as destination, then add the circuit to the circuits list
		if u == self.source and self.sourceVisited == True:
			self.circuits.append(circuit[:])
		else:
			self.sourceVisited = True
			# If current vertex is not destination
			# Recur for all the vertices adjacent to this vertex
			for i in self.graph[u]:
				if visited[i]== False or i == self.source:
					self.getAllCircuitsUtil(i, visited, circuit)				
		# Remove current vertex from circuit[] and mark it as unvisited
		circuit.pop()
		visited[u]= False
	# gets all circuits from 's' to 'd'
	def getAllCircuits(self):
		# Mark all the vertices as not visited
		visited =[False]*(self.V)
		circuit =[]
		# Call the recursive helper function to print all circuits
		self.getAllCircuitsUtil(self.source,visited,circuit)
		self.getAllHamiltonianCircuits()

#**********************************************************************************************************************

# Create a graph given in the above diagram
s = int(input("Enter source : "))
g = Graph(TSPcostMatrix,s)
g.getAllCircuits()
if not g.hamiltonianCircuits:
  print("Graph contains no hamiltonian circuits.")
else:
  print("Lowest Cost solution for travelling salesman : ")
  circuitIndices = g.lowestCostcircuit()
  for index in circuitIndices:
	  print(g.hamiltonianCircuits[index])
print("lowest cost is : " + str(g.lowestCost))
