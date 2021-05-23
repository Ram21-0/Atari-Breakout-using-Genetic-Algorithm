import pygame
import sys
from paddle import Paddle
from ball import Ball
from brick import Brick
from Config import * 
from train import (SPECIMENS_PER_GEN, INP_SIZE, HIDDEN_SIZE)
import pickle
import numpy as np
import copy
import math
import random
import threading
import time

pygame.init()

class Specimen:

	min_weight = -1
	max_weight = 1
	
	def __init__(self, gen, inputs, nr_layer1):
		self.gen = gen
		self.l1_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(inputs, nr_layer1))
		self.out_weights = np.random.uniform(low=Specimen.min_weight, high=Specimen.max_weight, size=(nr_layer1, 1))
		self.fitness = 0
		
	def output(self, input_vector):
		l1_out = np.matmul(input_vector, self.l1_weights)
		l1_out = relu(l1_out)
		return sigmoid(np.matmul(l1_out, self.out_weights))

def getInputVector(ball, paddle):
    temp = []
    temp.append(ball.rect.x)
    temp.append(ball.rect.y)
    temp.append(paddle.rect.x + paddle.width/2)		
    temp.append(paddle.width)
    return np.array(temp)

def sigmoid(x):
	return 1 / ( 1 + np.exp(-1 * x))

def relu(x):
    a = x
    a[x < 0] = 0
    return a

def getRandomIndex(numParents=numParents,probabilityPower=1.325):
    low = 0
    high = numParents - 1
    randomDouble = random.uniform(0,1)
    return int(low + (high + 1 - low) * (randomDouble**probabilityPower)) - 1

def breed(generation, genId):
    
    generation.sort(key = lambda x: x.fitness, reverse=True)

    saveWeights(DIRECTORY + "/best/gen" + str(genId) + ".pickle", np.array([generation[0].l1_weights, generation[0].out_weights, generation[0].fitness]))
    arr = []
    for sp in generation:
        arr.append(np.array([sp.l1_weights, sp.out_weights, sp.fitness]))
    saveWeights(DIRECTORY + "/all/allweights" + str(genId) + ".pickle", np.array(arr))    
    
    print('Best Fitness: ', generation[0].fitness)

    for childIndex in range(numParents,SPECIMENS_PER_GEN):

        fatherIndex = getRandomIndex()
        motherIndex = getRandomIndex()
        while fatherIndex == motherIndex:
            motherIndex = getRandomIndex()

        generation[childIndex] = twoPointCrossover(generation[fatherIndex],generation[motherIndex])

        mutate(generation,childIndex) 

    for i in range(len(generation)):
        generation[i].fitness = 0

def crossover(father,mother):
	child = Specimen(father.gen + 1, INP_SIZE, HIDDEN_SIZE)
	for i in range(len(father.l1_weights)):
		y = random.randint(0,99)
		child.l1_weights[i] = father.l1_weights[i] if y < 50 else mother.l1_weights[i]
	
	for i in range(len(father.out_weights)):
		y = random.randint(0,99)
		child.out_weights[i] = father.out_weights[i] if y < 50 else mother.out_weights[i]
	
	return child

def singlePointCrossover(father,mother):
	child = Specimen(father.gen+1,INP_SIZE,HIDDEN_SIZE)
	point = random.randint(0,len(father.l1_weights))
	child.l1_weights[:point] = father.l1_weights[:point]
	child.l1_weights[point:] = mother.l1_weights[point:]
	return child

def twoPointCrossover(father,mother):
	child = Specimen(father.gen+1,INP_SIZE,HIDDEN_SIZE)
	
	point1 = random.randint(0,len(father.l1_weights))
	point2 = random.randint(0,len(father.l1_weights))
	point1,point2 = min(point1,point2),max(point1,point2)
	child.l1_weights[:point1] = father.l1_weights[:point1]
	child.l1_weights[point1:point2] = mother.l1_weights[point1:point2]
	child.l1_weights[:point2] = father.l1_weights[:point2]

	point1 = random.randint(0,len(father.out_weights))
	point2 = random.randint(0,len(father.out_weights))
	point1,point2 = min(point1,point2),max(point1,point2)
	child.out_weights[:point1] = mother.out_weights[:point1]
	child.out_weights[point1:point2] = father.out_weights[point1:point2]
	child.out_weights[:point2] = mother.out_weights[:point2]

	return child

def avgCrossover(father,mother):
	child = Specimen(father.gen+1,INP_SIZE,HIDDEN_SIZE)
	child.l1_weights = (father.l1_weights + mother.l1_weights)/2
	child.out_weights = (father.out_weights + mother.out_weights)/2
	return child

def mutate(generation,childIndex):
    ind = random.randint(0,HIDDEN_SIZE-1) 
    for i in range(len(generation[childIndex].l1_weights)):
        generation[childIndex].l1_weights[i,ind] += random.uniform(-1,1)

    ind = random.randint(0,len(generation[childIndex].out_weights)-1)
    generation[childIndex].out_weights[ind,0] += random.uniform(-1,1)


## save and load weights

def saveWeights(filename, weights):
	with open(filename,'wb') as f:
		pickle.dump(weights, f)

def loadBestSpecimen(filename):
	bestSpecimen = Specimen(0,7,8)
	data = []
	with open(filename, "rb") as f:
		data = pickle.load(f)
	bestSpecimen.l1_weights = data[0]
	bestSpecimen.out_weights = data[1]
	bestSpecimen.fitness = data[2]
	return bestSpecimen

def loadAllSpecimen(filename):
	loadedGen = []
	data = []
	with open(filename,'rb') as f:
		data = pickle.load(f)
	
	for i in range(len(data)):
		spec = Specimen(i,7,8)
		spec.l1_weights = data[i][0]
		spec.out_weights = data[i][1]
		spec.fitness = data[i][2]
		loadedGen.append(spec)
	
	return loadedGen
            


    


