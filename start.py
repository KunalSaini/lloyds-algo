#! python

import csv
import glob
from os import system, name 

# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


def GetInputDataFile():
    clear()
    userInput = {}
    csvList = glob.glob("*.csv")
    print("select a data file to run Lloyd's algorithm")
    for idx, filePath in enumerate(csvList):
        print(f'({idx}) {filePath}')
    dataFileIndex = int(input("select option "))
    if 0 <= dataFileIndex < len(csvList):
        userInput["dataFile"] = csvList[dataFileIndex]
    else:
        GetInputDataFile()

    userInput["nbrOfClusters"] = int(input("enter number of clusters to compute "))
    return userInput

userInput = GetInputDataFile()
print(f"reading file from {userInput['dataFile']}")

with open(userInput["dataFile"], 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print(row)

## ramdomly select K starting points
## Assign each point to one of the K clusters
## compute mean of each cluster, make that the new starting points
## repeat unit no change in clusters

