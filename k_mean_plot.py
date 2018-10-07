import k_mean
import math
import numpy as np 
import random
from matplotlib.patches import Circle
from matplotlib import pyplot

##Cut down the items to two dimension
def MakeTwoDim(items, indexA, indexB):
	n = len(items)
	X = [];

	for i in range(n):
		item = items[i]
		newItem = [item[indexA], item[indexB]]
		X.append(newItem)
	return X

## find radius from two array
def Radius(cluster, mean):
	distances = []
	for point in cluster:
		distances.append(k_mean.EuclideanDistance(point, mean))
	#print(distances)

	if(len(distances) == 0):
		print(cluster)
		print('1 or less point in cluster, use less number of cluster or try again')
		print('mean', mean)
		#raise Exception('1 or less point in cluster, use less number of cluster or try again')
		
	radius = max(val for (idx, val) in enumerate(distances))
	if(radius == None):
		return 1
	else:
		return radius


##plot clusters
def PlotClusters(means, clusters):
	pyplot.figure()
	n = len(clusters)
	colors = ['r', 'b', 'g', 'y', 'c', 'm', 'k']

	for i in range(n):
		cluster = clusters[i]
		mean = means[i]
		c = random.choice(colors)
		colors.remove(c)

		Xa = []
		Xb = []
		for item in cluster:
			Xa.append(item[0])
			Xb.append(item[1])

		radius = Radius(cluster, mean)
		#print(mean[0], mean[1], radius)
		ax = pyplot.gca()
		disk1 = pyplot.Circle((mean[0], mean[1]), radius, color=c, fill=False)
		ax.add_artist(disk1)
		pyplot.plot(Xa, Xb, 'o', color=c)

	pyplot.show(block=False)



def main():
	items = k_mean.ReadData('grid.txt')
	#print(items)
	#items = MakeTwoDim(items, 2, 3) #karray index of features to keep, use when more than 2d
	#print(items)

	k = 4
	means = k_mean.CalculateMeans(k, items)
	clusters = k_mean.FindClusters(means, items)

	PlotClusters(means, clusters)

if __name__ == '__main__':
	main()
