# encoding: utf-8
import sys
import random
import math

import xlrd
import k_mean_plot as kmp
import k_mean as km
from matplotlib import pyplot
import animation as anm
import drone_model as dm


def CalculateBatteryWeight(Soln, VRP):
	path_length = len(Soln) #included depot point
	n = len(VRP['nodes'])
	path_demand = []  ##Extracting the demand of each point of the path
	for item in Soln:
		for i in range(n):
			if ((VRP['nodes'][i]['posX'] == item[0]) & (VRP['nodes'][i]['posY'] == item[1])):
				path_demand.append(VRP['nodes'][i]['demand'])
	print(path_demand)
	amp_rating = 0

	payload = sum(path_demand)
	for i in range(len(path_demand)-1):
		distance = 1000* km.EuclideanDistance(Soln[i], Soln[i+1]) ##convert into meter
		#print("payload is: ", payload - path_demand[i])
		amp_rating += dm.AmpRate(payload - path_demand[i], distance)

	battery_weight = dm.BatWeight(amp_rating)
	print("amp_rating", amp_rating)
	print("battery weight ", battery_weight)

	## computing total cost for each path
	cost = 0
	for i in range(len(path_demand)-1):
		distance = 1000* km.EuclideanDistance(Soln[i], Soln[i+1]) ##convert into meter
		#print("payload is: ", payload - path_demand[i])
		cost += dm.Cost(amp_rating, battery_weight, payload-path_demand[i], distance)

	print("Total cost on path:", cost)
	return 0


def GridData(vrp):
	##function to give only 2D data as [[x1,y1], [x2, y2], ...[xn,yn]] which is required in k_mean_plot
	Grid = []
	#print("vrp", vrp['nodes'])
	n = len(vrp['nodes'])  # departure point included
	#print("vrp length", n)
	for i in range(1, n):
		Grid.append([vrp['nodes'][i]['posX'], vrp['nodes'][i]['posY']])
		#print(i-1, 'th enetry in grid', Grid[i-1])

	#print("grid in function", Grid)
	return Grid


def ClusterVrp(vrp, cluster, capacity):
	#print(vrp['nodes'])
	#print(len(vrp['nodes']))
	#print(cluster)

	new_vrp = {}
	new_vrp['nodes'] = [{'posY': 0, 'posX': 0, 'demand': 0, 'label': 'depot'}]
	#print(vrp.keys())
	n = len(vrp['nodes'])
	
	
	#print(cluster)
	#print(vrp['nodes'])
	for i in range(n):
		for item in cluster:
			if ((vrp['nodes'][i]['posX'] == item[0]) & (vrp['nodes'][i]['posY'] == item[1])):
				new_vrp['nodes'].append(vrp['nodes'][i])
	new_vrp['capacity'] = capacity
	#print(len(list(new_vrp['nodes'])))
	#print(list(new_vrp.keys()))
	#print(new_vrp['nodes'])
	#print("done")
	return new_vrp


def ReadFile(filename):
	#file syntax nodeNo, demand, y, x
	VRS = {}
	VRS['nodes'] = []
	VRS['nodes'].append({'posY': 0, 'posX': 0, 'demand': 0, 'label': 'depot'})
	VRS['capacity'] = 100
	wb = xlrd.open_workbook(filename)
	sheet = wb.sheet_by_index(0)
	sheet.cell_value(0,0)
	n = sheet.nrows
	for i in range (n):
		temp_dict = {'posY': float(sheet.cell_value(i,3)), 'posX': float(sheet.cell_value(i,2)), 'demand': float(sheet.cell_value(i,1)), 'label': sheet.cell_value(i,0)}
		VRS['nodes'].append(temp_dict)
	return VRS


def distance(n1, n2):
	#Eucledian distance
	dx = n2['posX'] - n1['posX']
	dy = n2['posY'] - n1['posY']
	return math.sqrt(dx * dx + dy * dy)


def fitness(vrp, p):
	# The first distance is from depot to the first node of the first route
	s = distance(vrp['nodes'][0], vrp['nodes'][p[0]])
	# Then calculating the distances between the nodes
	for i in range(len(p) - 1):
		prev = vrp['nodes'][p[i]]
		next = vrp['nodes'][p[i + 1]]
		s += distance(prev, next)
	# The last distance is from the last node of the last route to the depot
	s += distance(vrp['nodes'][p[len(p) - 1]], vrp['nodes'][0])
	return s


def adjust(vrp, p):
	# Adjust repeated
	repeated = True
	while repeated:
		repeated = False
		for i1 in range(len(p)):
			for i2 in range(i1):
				if p[i1] == p[i2]:
					haveAll = True
					for nodeId in range(len(vrp['nodes'])):
						if nodeId not in p:
							p[i1] = nodeId
							haveAll = False
							break
					if haveAll:
						del p[i1]
					repeated = True
				if repeated: break
			if repeated: break
	# Adjust capacity exceed
	i = 0
	s = 0.0
	#print(list(vrp.keys()))
	cap = vrp['capacity']
	while i < len(p):
		s += vrp['nodes'][p[i]]['demand']
		if s > cap:
			p.insert(i, 0)
			s = 0.0
		i += 1
	i = len(p) - 2
	# Adjust two consective depots
	while i >= 0:
		if p[i] == 0 and p[i + 1] == 0:
			del p[i]
		i -= 1


def SolveGenetic(vrp):

	popsize = int(sys.argv[1])
	iterations = int(sys.argv[2])

	pop = []

	# Generating random initial population
	for i in range(popsize):
		p = list(range(1, len(vrp['nodes'])))
		random.shuffle(p)
		pop.append(p)
	for p in pop:
		adjust(vrp, p)

	# Running the genetic algorithm
	for i in range(iterations):
		nextPop = []
		# Each one of this iteration will generate two descendants individuals. Therefore, to guarantee same population size, this will iterate half population size times
		for j in range(int(len(pop) / 2)):
			# Selecting randomly 4 individuals to select 2 parents by a binary tournament
			parentIds = set()
			while len(parentIds) < 4:
				parentIds |= {random.randint(0, len(pop) - 1)}
			parentIds = list(parentIds)
			# Selecting 2 parents with the binary tournament
			parent1 = pop[parentIds[0]] if fitness(vrp, pop[parentIds[0]]) < fitness(vrp, pop[parentIds[1]]) else pop[parentIds[1]]
			parent2 = pop[parentIds[2]] if fitness(vrp, pop[parentIds[2]]) < fitness(vrp, pop[parentIds[3]]) else pop[parentIds[3]]
			# Selecting two random cutting points for crossover, with the same points (indexes) for both parents, based on the shortest parent
			cutIdx1, cutIdx2 = random.randint(1, min(len(parent1), len(parent2))-1), random.randint(1, min(len(parent1), len(parent2))-1)
			cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)
			# Doing crossover and generating two children
			child1 = parent1[:cutIdx1] + parent2[cutIdx1:cutIdx2] + parent1[cutIdx2:]
			child2 = parent2[:cutIdx1] + parent1[cutIdx1:cutIdx2] + parent2[cutIdx2:]
			nextPop += [child1, child2]
		# Doing mutation: swapping two positions in one of the individuals, with 1:15 probability
		if random.randint(1, 15) == 1:
			ptomutate = nextPop[random.randint(0, len(nextPop) - 1)]
			i1 = random.randint(0, len(ptomutate) - 1)
			i2 = random.randint(0, len(ptomutate) - 1)
			ptomutate[i1], ptomutate[i2] = ptomutate[i2], ptomutate[i1]
		# Adjusting individuals
		for p in nextPop:
			adjust(vrp, p)
		# Updating population generation
		pop = nextPop

	# Selecting the best individual, which is the final solution
	better = None
	bf = float('inf')
	for p in pop:
		f = fitness(vrp, p)
		if f < bf:
			bf = f
			better = p
	return better, bf

def GetSoln(VRP, MaxDrones, Kmax):
	grid = GridData(VRP)
	Paths = []
	TotalDrones = []
	Distances = []
	Clusters = []
	Solution = []
	for j in range(1, Kmax+1):
		k = j
		#print("k value", k)
	
		## something wrong here
		means = km.CalculateMeans(k, grid)

		clusters = kmp.k_mean.FindClusters(means, grid)

		kmp.PlotClusters(means, clusters)

		
		path_solns = []
		drone_sum = 0
		temp_clusters = []	
		total_temp = 0
		for i in range(k):
			vrp = ClusterVrp(VRP, clusters[i], 100) #capacity 100
			temp_better, temp_bf = SolveGenetic(vrp)

			##printing the solution
			#print('for k ',k,'and i ',i)
			#print(' route-> ')
			#print('depot')
			count = 1
			if(temp_better[0] == 0):
				temp_better.remove(0)

			last_index = len(temp_better) -1
			if(temp_better[last_index] == 0):
				temp_better.pop(last_index)

			for nodeIdx in temp_better:
				#print (vrp['nodes'][nodeIdx]['label'])
				if(vrp['nodes'][nodeIdx]['label'] == 'depot'):
					count += 1

			#print('depot')
			#print("Drone required ", count)
			drone_sum += count
			total_temp += temp_bf
			temp_clusters.append(vrp)
			path_solns.append(temp_better)
			#print(' cost ')
			#print ('%f' % temp_bf)
		
		Paths.append(path_solns)
		Clusters.append(temp_clusters)
		TotalDrones.append(drone_sum)
		Distances.append(total_temp)
 
		#print(total_temp)

	index = Distances.index(min(Distances))

	feasibleSolIndex = []
	feasibleCosts = []


	for i in range(2):
		if(TotalDrones[i] <= MaxDrones):
			feasibleSolIndex.append(i)

	SolIndex = float('Inf')
	OptimumDistance = float('Inf')
	for i in feasibleSolIndex:
		if(Distances[i] <= OptimumDistance): 
			OptimumDistance = Distances[i]
			SolIndex = i

	#print("Feasible Cost ", OptimumDistance)
	#print("Feasible Sol Index", index)


	##printing optimal solution
	#print(Paths[index])
	#print("\n Printing the optimal path in terms of node")
	Feasible_k_value = len(Clusters[index])
	TotalRouts = 0

	for i in range(Feasible_k_value):
		cluster_paths = []
		#print(' route->', TotalRouts)
		m = 0
		#print('depot')
		count = 1
		path = []
		path.append([0,0])

		for nodeIdx in Paths[index][i]:
			point = []
			#print (Clusters[index][i]['nodes'][nodeIdx]['label'])
			point.append(Clusters[index][i]['nodes'][nodeIdx]['posX'])
			point.append(Clusters[index][i]['nodes'][nodeIdx]['posY'])
			path.append(point)

			if(Clusters[index][i]['nodes'][nodeIdx]['label'] == 'depot'):
				#print(' route->', count+TotalRouts)
				cluster_paths.append(path)
				path = []
				path.append([0,0])
				count += 1			
				#print('depot')

		path.append([0,0])
		cluster_paths.append(path)
		Solution.append(cluster_paths)

		#print('depot')
		#print('count', count)
		TotalRouts += count

	#print(Solution)
	return Feasible_k_value, TotalDrones,OptimumDistance, Solution



def main():

	filename = sys.argv[3]
	VRP = ReadFile(filename) #this function reads entire file and all data
	VRP['capacity'] = 100 
	MaxDrones = float(sys.argv[4])
	Kmax = int(sys.argv[5])
	Grid = GridData(VRP)
	speed = int(sys.argv[6]) #speed to controla animated result

	Feasible_k_value, TotalDrones, OptimumDistance, Solution = GetSoln(VRP, MaxDrones, Kmax)
	#print(Solution)
	print("Feasible k value ", Feasible_k_value)
	
	# finding cost using drone model
	#Print ("Printing the optimal path in terms of Coordinates")
	battery_array = []

	for i in range(Feasible_k_value):
		print(len(Solution[i]))
		print("Cluster Id:", i+1)
		for j in range(len(Solution[i])):
			print("path:", j+i+1) 
			#print(Solution[i][j])
			battery_array.append(CalculateBatteryWeight(Solution[i][j], VRP))
			for k in range(len(Solution[i][j])):
				print(Solution[i][j][k][0], Solution[i][j][k][1])
				print("->")

	means = km.CalculateMeans(Feasible_k_value, Grid)

	clusters = kmp.k_mean.FindClusters(means, Grid)
	anm.main(speed, means, clusters, Solution)

	pyplot.show()



if __name__ == '__main__':
	main()

