from src.utils.generator import generateRandomPoints

def calculatePi(numberOfPoints):
  
  pointsInsideTheCircle = 0

  for x, y in generateRandomPoints(numberOfPoints):
    if x**2 + y**2 <= 1:
      pointsInsideTheCircle += 1
  

  estimatedPi = 4 * (pointsInsideTheCircle/ float(numberOfPoints))
  return estimatedPi