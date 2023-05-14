from random import uniform
import numpy as np
from matplotlib import pyplot as plt
import math

###################################################### Defining Consants #########################################################

a = -10 # -10 m/s^2 overall acceleration (area under curve)
v = 5 # initial velocity ⚠️ VELOCITY IS GLOBAL
DeltaT = 1.5 # Duration of collision
CollisionStart = 7 # Number of seconds after program starts that collision starts
r = 0.1 # Rate of sensor recordings (e.g. every 0.05 seconds)

###################################################### Defining Basic Functions #########################################################

def sensorAccel(t):
    global a, v, DeltaT, CollisionStart

    uncertainty = 0.09 #5% error
    aGraph = (2*a)/DeltaT
    if (t < CollisionStart) or (t >= (DeltaT + CollisionStart)):
        return uniform(-(uncertainty**2), uncertainty**2), uncertainty**4 #Returns mean accel and variance
    else:
        accel = (-aGraph/DeltaT)*(t-CollisionStart)+aGraph
        return uniform(accel - uncertainty*accel, accel + uncertainty*accel), (uncertainty*accel)**2 # Returns mean accel and variance

def sensorPos(oldVelocity, oldPos, meanAccel, varianceAccel):
    global r

    newVelocity = (meanAccel * r) + oldVelocity
    sensorPos = oldPos + ((r*abs(newVelocity-oldVelocity))/2) + (r*newVelocity)
    variancePos = varianceAccel * (r**2)
    return newVelocity, sensorPos, variancePos

#Assumes constant positive velocity
def predictPos(fusedMean, fusedVariance):
    u = 5 #Set velocity

    nextPosition = fusedMean + (u*r)
    return nextPosition, fusedVariance #Uncertainty is variance, remember to square root to use | Returns mean position and variance

def fusedPosition(meanSensor, varianceSensor, meanPredicted, variancePredicted):
    fusedPos = ((meanSensor*varianceSensor) + (meanPredicted*variancePredicted))/(varianceSensor + variancePredicted)
    fusedVariance = (varianceSensor*variancePredicted)/(varianceSensor + variancePredicted)
    return fusedPos, fusedVariance

###################################################### Test Running #################################################################

########For graphing
time = [0]

x = [0]
variancePos = 0
T = 20 #Length of time program runs (seconds)
t = 0 #Time (s)

#Two series: predicted and recorded
while t <= T:
    predictedPos, predictedVariance = predictPos(x[-1], variancePos)
    accel, accelVariance = sensorAccel(t)
    v, measuredPos, variancePos = sensorPos(v, x[-1], accel, accelVariance)
    fusedPos, fusedVariance = fusedPosition(measuredPos, variancePos, predictedPos, predictedVariance)
    x.append(fusedPos) #⚠️ Change to test each of measuredPos, predictedPos and fusedPos

    time.append(t)
    t += r

###################################################### Graphing #############################################################################

plt.xlabel("Time (s)") 
plt.ylabel("Position (m)") 
plt.plot(time, x, 'o') 
print(x)
plt.show()