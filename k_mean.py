import math
import csv
import sys
import random


##Read the data
def ReadData(fileName):
    #Read the file, splitting by lines
    f = open(fileName,'r');
    lines = f.read().splitlines();
    f.close();

    items = [];

    for i in range(len(lines)):
        line = lines[i].split(',');
        #print(line)
        itemFeatures = [];

        for j in range(len(line)):
            v = float(line[j]); #Convert feature value to float
            itemFeatures.append(v); #Add feature value to dict

        #print(itemFeatures)
        items.append(itemFeatures);
        #print(items)

    random.shuffle(items);

    #print(items)

    return items;



#Finding minima and maxima of each feature in given items
def FindFeatureRange(items):

	No_features = len(items[0])
	minima = [sys.maxsize for i in range(No_features)]
	maxima = [-sys.maxsize -1 for i in range(No_features)]

	for item in items:
		for i in range(len(item)):
			if(item[i] < minima[i]):
				minima[i] = item[i]

			if(item[i] > maxima[i]):
				maxima[i] = item[i]

	return minima, maxima


## Eucledian distance
def EuclideanDistance(x, y):
	Dist = 0;
	for i in range(len(x)):
		Dist = Dist + math.pow(x[i]-y[i], 2)
	return math.sqrt(Dist);


## Compute mean valuesa
def Mean(z):
	mean = 0;
	points = len(z)
	for point in z:
		mean = mean+point

	mean = mean/points
	return mean


##Initialise the chosen k mean values randomly 
def InitializeMeans(items, k, cMin, cMax):
	# for each cluster assign the random values of features in limit of min and max valuesFirst method to initialize mean
	No_features = len(items[0])
	means = [[0 for i in range(No_features)] for j in range(k)]

	for mean in means:
		for i in range(len(mean)):
			mean[i] = random.uniform(cMin[i]+0.1, cMax[i]-0.1) #avoid larger range

	return means
	'''
	##second way where assign data from items itself
	k_index = random.sample(range(0, len(items)), k)

	means = []
	for i in range(k):
		means.append(items[k_index[i]])
	return means
	'''

##Update the mean values
def UpdateMean(n, mean, item):
	for i in range(len(mean)):
		m = mean[i]
		m = (m*(n-1) + item[i])/float(n);
		mean[i] = round(m, 3);
	return mean


## Classify the items in clusters
def AssignCluster(means, data_point):
	distances = []
	for i in range(len(means)):
		distances.append(EuclideanDistance(means[i], data_point)) 
	
	cluster_index = min((val, idx) for (idx, val) in enumerate(distances))[1] #storing id of min value
	return cluster_index
	

## Find cluster given the means and items
def FindClusters(means, items):
	clusters = [[] for i in range(len(means))]
	#print("items which should be grid", items)
	for item in items:

		#classify that item into a cluster
		index = AssignCluster(means, item)
		#print("index value for item", item, "is", index)

		# Add item to cluster
		clusters[index].append(item)

	return clusters


##Loop through the mean updating process
def CalculateMeans(k, items, maxIterations = 100000):
	
	#find maxima and minima for columns
	cMin, cMax = FindFeatureRange(items)

	#initialize means at random points
	means = InitializeMeans(items, k, cMin, cMax)

	#array to hold the number of item in each cluster
	clusterSizes = [0 for i in range(len(means))]

	#An array to hold the cluster where each item belong to
	belongTo = [0 for i in range(len(items))]

	# calculate means
	for e in range(maxIterations):


		#if no change in cluster occur halt the process
		noChange = True

		for i in range(len(items)):
			item = items[i]

			# classify that item into a cluster
			index = AssignCluster(means, item)
			clusterSizes[index] += 1
			cSize = clusterSizes[index]
			means[index] = UpdateMean(cSize, means[index], item)

			# Item changed cluster
			if(index != belongTo[i]):
				noChange = False

			belongTo[i] = index #putting that item into new cluster


		#nothing happened, return
		if(noChange):
			break

	#print(means)
	return means;

if __name__ == '__main__':
	main()
