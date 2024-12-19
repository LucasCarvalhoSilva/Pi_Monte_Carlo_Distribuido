import random

def generateRandomPoints(numberOfPoints):

  for _ in range (numberOfPoints):
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    yield x, y