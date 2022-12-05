import sys # Library for INT_MAX
import numpy as np

class Graph():

	def __init__(self, vertices):		# vertices: 정점 배열
		self.V = len(vertices)
		self.vertices = vertices
		self.graph = [[0 for column in range(self.V)]
					for row in range(self.V)]
		self.result_graph = np.zeros((self.V, self.V))

	# A utility function to print the constructed MST stored in parent[]
	def printMST(self, parent):
		print("Edge \tWeight")
		for i in range(1, self.V):
			print(parent[i], "-", i, "\t", self.graph[i][parent[i]])

	def saveMST(self, parent):
		for i in range(1, self.V):
			p = parent[i]
			self.result_graph[p, i] = self.graph[i][p]
			self.result_graph[i, p] = self.graph[i][p]

		# print("결과", self.result_graph)
		# np.savetxt('data/exec_prim.csv', self.result_graph,delimiter=",")
		return self.result_graph

	def minKey(self, key, mstSet):

		# Initialize min value
		min = sys.maxsize

		for v in range(self.V):
			if key[v] < min and mstSet[v] == False:
				min = key[v]
				min_index = v

		return min_index

	def primMST(self):

		# Key values used to pick minimum weight edge in cut
		key = [sys.maxsize] * self.V

		parent = [None] * self.V # Array to store constructed MST
		# Make key 0 so that this vertex is picked as first vertex
		key[0] = 0
		mstSet = [False] * self.V


		parent[0] = -1 # First node is always the root of

		for cout in range(self.V):

			# Pick the minimum distance vertex from
			u = self.minKey(key, mstSet)

			mstSet[u] = True

			for v in range(self.V):

				if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
					key[v] = self.graph[u][v]
					parent[v] = u

		# self.printMST(parent)
		return self.saveMST(parent)


# Driver's code
if __name__ == '__main__':
	g = Graph([1,2,3,4,5])
	g.graph = [[0, 2, 0, 6, 0],
			[2, 0, 3, 8, 5],
			[0, 3, 0, 0, 7],
			[6, 8, 0, 0, 9],
			[0, 5, 7, 9, 0]]

	g.primMST()
