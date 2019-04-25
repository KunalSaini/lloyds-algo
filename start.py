#! python

import csv
import glob
import random
import math
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from os import system, name 


def clear():
    '''
    define console clear function
    '''
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def GetInputDataFile():
    '''
    get user input for which data file to run algo on
    also get number of centroids
    '''
    clear()
    dataFile = None
    k = None
    csvList = glob.glob("data/*.csv")
    print("select a data file to run Lloyd's algorithm")
    for idx, filePath in enumerate(csvList):
        print(f'({idx}) {filePath}')
    dataFileIndex = int(input("select option "))
    if 0 <= dataFileIndex < len(csvList):
        dataFile = csvList[dataFileIndex]
    else:
        GetInputDataFile()

    k = int(input("enter number of clusters to compute "))
    return (dataFile, k)


def GetDistance(x, y):
    '''
    calculate Euclidean distance between two n dimentional points
    '''
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


def Assign(centroides, data):
    '''
    Assign each point to one of the k clusters
    '''
    mapping = []
    for point in data:
        computedMap = {
            'closestDistance' : None,
            'closestCentroid' : None,
            'point' : point,
        }
        for centroid in centroides:
            distance = GetDistance(point, centroid)
            if computedMap['closestDistance'] == None or computedMap['closestDistance'] > distance :
                computedMap['closestDistance'] = distance
                computedMap['closestCentroid'] = centroid

        mapping.append(computedMap)
    return mapping

def sumPoints(x1,x2):
    return [(x1[0]+x2[0]),(x1[1]+x2[1])]

def Update(centroides, previousIterationData):
    '''
    calculate new centroid based on clusters
    '''
    ## compute mean of each cluster, make that the new starting points
    differenceVector = []
    newCentroides = []
    for centroid in centroides:
        cdata = [y['point'] for y in list(filter(lambda x: x['closestCentroid'] == centroid, previousIterationData))]
        totalVector = reduce(sumPoints, cdata)
        mean = [x / len(cdata) for x in totalVector]
        print(f'number of data points for {centroid} are {len(cdata)} with mean {mean}')

        newCentroides.append(mean)
        distance = GetDistance(mean, centroid)
        differenceVector.append(distance)
    return (newCentroides, differenceVector)



def plotAndSave(nbr, centroides, mapped):
    '''
    create scatter plot
    '''
    nbrFormat = '{:0>3}'.format(nbr)
    title = 'Iteration.' + nbrFormat
    fig, ax = plt.subplots(1, figsize=(10, 6))
    ax.set(title=title)
    for idx, centroid in enumerate(centroides):
        cluster = [y['point'] for y in list(filter(lambda x: x['closestCentroid'] == centroid, mapped))]
        x = [i[0] for i in cluster]
        y = [i[1] for i in cluster]
        ax.scatter(x, y, color=colors[idx+10])
        ax.scatter(centroid[0], centroid[1], color='black', s=50)
        ax.grid(True)
    fig.tight_layout()
    plt.savefig(f'images/{title}.png')
    plt.close()


def CalculatePartitions(data, k, epsilon, maxIterations):
    '''
    cluster data in k centroids based on lloyds algorithm
    '''
    ## ramdomly select K starting points to start
    centroides = random.sample(data, k)
    print(f'assigning {len(data)} number of data points to {k} clusters')
    mapped = Assign(centroides, data)
    significientDifference = True
    itr=1
    ## repeat unit no change in clusters
    while significientDifference:
        print('iteration', itr)
        plotAndSave(itr, centroides, mapped)
        itr += 1
        newCentroides, diffVector = Update(centroides, mapped)
        if sum(diffVector) < epsilon or itr > maxIterations:
            significientDifference = False
        if significientDifference:
            centroides = newCentroides
            mapped = Assign(centroides, data)

if __name__ == "__main__":
    dataFile, k = GetInputDataFile()
    print(f"reading file from {dataFile}")
    data = []
    with open(dataFile, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            dataRow = [float(row[0]),float(row[1])]
            #dataRow.append(float(row[0]))
            #dataRow.append(float(row[1]))
            data.append(dataRow)

    EPSILON = 10**-5
    MAX_ITERATIONS = 30
    colors = list(mcolors.CSS4_COLORS.keys())
    CalculatePartitions(data, k, EPSILON, MAX_ITERATIONS)