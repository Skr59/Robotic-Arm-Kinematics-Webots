import math
import matplotlib.pylab as plt
theta1=30
theta2=60
t1=math.radians(theta1)
t2=math.radians(theta2)
L1=5
L2=7
x0=0
y0=0
x1=L1*math.cos(t1)
y1=L2*math.sin(t1)
x2=x1+L2*math.cos(t1+t2)
y2=y1+L2*math.sin(t1+t2)
plt.figure(figsize=(8, 7))

plt.plot([x0, x1], [y0, y1], 'b-o',
         linewidth=3, markersize=10, label="Link 1")

plt.plot([x1, x2], [y1, y2], 'r-o',
         linewidth=3, markersize=10, label="Link 2")

# Display joints
plt.scatter(x2, y2, color='green',
            s=150, label="End Effector")
plt.text(x0, y0, "Base")
plt.text(x1, y1, "Elbow")
plt.text(x2, y2, "End Effector")

# Graph settings
plt.title("2D Robotic Arm Simulation")
plt.xlabel("X Position")
plt.ylabel("Y Position")

plt.xlim(-13, 13)
plt.ylim(-13, 13)

plt.grid(True)
plt.axhline(0)
plt.axvline(0)

plt.legend()
plt.axis("equal")
plt.show()