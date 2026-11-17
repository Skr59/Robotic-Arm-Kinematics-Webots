import math 
def forward_kinematics(theta1,theta2,L1,L2):
        theta1_rad=math.radians(theta1)
        theta2_rad=math.radians(theta2)
        x=(L1*math.cos(theta1_rad)+L2*math.cos(theta1_rad+theta2_rad))
        y=(L1*math.sin(theta1_rad)+L2*math.sin(theta1_rad+theta2_rad))
        return x, y
L1=5
L2=4
positions=[
        (60,40),
        (30,50),
        (60,70)

]
for theta1,theta2 in positions:
        x,y=forward_kinematics(L1,L2,theta1,theta2)
        print("joints Angles:",theta1,theta2)
        print("X Position:",round(x,3))
        print("Y Position:",round(y,3))
        print("-----------------------------")