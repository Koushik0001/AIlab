#********************************************************************************************************************* 
# 											*** AI lab (2022-2023) ***	
# 	
#	DATE		:	04/08/2022
# 	NAME 		:	KOUSHIK MAHANTA 
# 	CLASS ROLL	:	002011001106
#	DEPARTMENT 	:	INFORMATION TECHNOLOGY
#	YEAR		:	3rd
#	COURSE		: 	UG
#
#*********************************************************************************************************************
#
#	ASSIGNMENT 1: This program prints lowest cost circuit from source to destination from a costmatrix of a weighted graph
#
#**********************************************************************************************************************

from dataclasses import field
import numpy as np
from collections import defaultdict

CSVData = open("testmatrix.csv")
costMatrix = np.loadtxt(CSVData, delimiter=" ")

#**********************************************************************************************************************
#**********************************************************************************************************************
# 
#             This program prints lowest cost path from source to destination from a costmatrix of a weighted graph
#
#
#This class represents a graph
# using adjacency list representation
class Graph:

	def __init__(self, myCostMatrix):
		# No. of vertices
		self.V = len(myCostMatrix)
		self.costMatrix = myCostMatrix
		# default dictionary to store graph
		self.graph = defaultdict(list)
		self.paths = list(list())
		self.addEdge()
		self.lowestCost = 0

	# function to add edges to a graph
	def addEdge(self):
		for i in range(0, self.V):
			for j in range(0, self.V):
				if self.costMatrix[i][j] != -1 :
					self.graph[i].append(j)
				

	#function to find the lowest Cost to travel from source to destination and
	#getting the lowest cost path
	def lowestCostPath(self):
		indexOfLowestCostPaths = []
		self.lowestCost = 0
		index = 0
		for path in self.paths:
			i = 0
			current = path[i]
			next = path[i+1]
			totalcost = 0
			while current != path[-1]:
				totalcost += self.costMatrix[current][next]
				i+=1
				current = path[i]
				if current != path[-1]:
					next = path[i+1]
				print(self.lowestCost)
			if index == 0:
				self.lowestCost = totalcost
			if totalcost < self.lowestCost:
				self.lowestCost = totalcost
				indexOfLowestCostPaths.clear()
				indexOfLowestCostPaths.append(index)
			elif totalcost == self.lowestCost:
				indexOfLowestCostPaths.append(index)
			index += 1
		return indexOfLowestCostPaths


	'''A recursive function to print all paths from 'u' to 'd'.
	visited[] keeps track of vertices in current path.
	path[] stores actual vertices and path_index is current
	index in path[]'''
	def getAllPathsUtil(self, u, d, visited, path):
		# Mark the current node as visited and store in path
		visited[u]= True
		path.append(u)
		# If current vertex is same as destination, then add the path to the paths list
		if u == d:
			self.paths.append(path[:])
		else:
			# If current vertex is not destination
			# Recur for all the vertices adjacent to this vertex
			for i in self.graph[u]:
				if visited[i]== False:
					self.getAllPathsUtil(i, d, visited, path)				
		# Remove current vertex from path[] and mark it as unvisited
		path.pop()
		visited[u]= False


	# gets all paths from 's' to 'd'
	def getAllPaths(self, s, d):
		# Mark all the vertices as not visited
		visited =[False]*(self.V)
		path =[]
		# Call the recursive helper function to print all paths
		self.getAllPathsUtil(s, d, visited,path)

#**********************************************************************************************************************

# Create a graph given in the above diagram
g = Graph(costMatrix)
s = int(input("Enter source : "))
d = int(input("Enter destination : "))
g.getAllPaths(s, d)
print("Lowest Cost path/paths is/are : ")
pathIndices = g.lowestCostPath()
for index in pathIndices:
	print(g.paths[index])
print("lowest cost is : " + str(g.lowestCost))
