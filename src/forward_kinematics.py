import math 
# link lengths
L1=5
L2=4
#joint angles in degrees
theta1 =45
theta2=40
# convert angles into radians
theta1_rad=math.radians(theta1)
theta2_rad=math.radians(theta2)
# calculate  the shoulder value in x axis 
x=L1*math.cos(theta1_rad)+L2*math.cos(theta1_rad+theta2_rad)
#calculate the elbow value in the y axis
y=L1*math.sin(theta1_rad)+L2*math.sin(theta1_rad+theta2_rad)
#display the result of the forward kinematicks
print("Robotics Arm and forrwardkinematics")
print("--------------------------------")
print ("joint 1 angle:",theta1,"degrees")
print( "joint 2 angle:",theta2,"degrees")
print("End Effector X:",round(x,3))
print("End Effector Y:",round(y,3))
