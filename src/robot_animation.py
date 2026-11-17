
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sqlalchemy import false

# =====================================
# PART 1: ROBOT CONFIGURATION
# =====================================

L1 = 5
L2 = 7

# Target position
target_x = 4
target_y = 8

# =====================================
# PART 2: INVERSE KINEMATICS
# =====================================

D = (
    target_x**2 + target_y**2 - L1**2 - L2**2
) / (2 * L1 * L2)

# Check reachability
if D < -1 or D > 1:
    raise ValueError("Target position is unreachable!")

# Calculate elbow angle
theta2_target = math.acos(D)

# Calculate shoulder angle
k1 = L1 + L2 * math.cos(theta2_target)
k2 = L2 * math.sin(theta2_target)

theta1_target = (
    math.atan2(target_y, target_x)
    - math.atan2(k2, k1)
)

# =====================================
# PART 3: STARTING JOINT ANGLES
# =====================================

theta1_start = 0
theta2_start = 0

# =====================================
# PART 4: CREATE GRAPH
# =====================================

fig, ax = plt.subplots(figsize=(8, 7))

ax.set_title("Animated 2D Robotic Arm")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

ax.set_xlim(-13, 13)
ax.set_ylim(-13, 13)

ax.grid(True)
ax.axhline(0)
ax.axvline(0)

ax.set_aspect("equal")

# Show target position
ax.plot(
    target_x, target_y,
    "g*", markersize=15,
    label="Target Position"
)

# Create robot links
link1, = ax.plot(
    [], [], "b-o",
    linewidth=5,
    markersize=9,
    label="Link 1"
)

link2, = ax.plot(
    [], [], "r-o",
    linewidth=5,
    markersize=9,
    label="Link 2"
)

# Display joints
joints, = ax.plot(
    [], [], "ko",
    markersize=7,
    label="Robot Joints"
)

# Display angle information
info = ax.text(
    0.02, 0.95, "",
    transform=ax.transAxes
)

ax.legend()

# =====================================
# PART 5: ANIMATION FUNCTION
# =====================================

def update(frame):

    # Calculate animation progress
    alpha = frame / 100

    # Gradually change joint angles
    theta1 = (
        theta1_start
        + alpha * (theta1_target - theta1_start)
    )

    theta2 = (
        theta2_start
        + alpha * (theta2_target - theta2_start)
    )

    # Convert angles into radians
    t1 = theta1
    t2 = theta2

    # Calculate shoulder position
    x1 = L1 * math.cos(t1)
    y1 = L1 * math.sin(t1)

    # Calculate end effector position
    x2 = x1 + L2 * math.cos(t1 + t2)
    y2 = y1 + L2 * math.sin(t1 + t2)

    # Update first link
    link1.set_data(
        [0, x1],
        [0, y1]
    )

    # Update second link
    link2.set_data(
        [x1, x2],
        [y1, y2]
    )

    # Update joint positions
    joints.set_data(
        [0, x1, x2],
        [0, y1, y2]
    )

    # Display current angles
    info.set_text(
        f"Shoulder: {math.degrees(t1):.1f}°\n"
        f"Elbow: {math.degrees(t2):.1f}°"
    )

    return link1, link2, joints, info


# =====================================
# PART 6: START ANIMATION
# =====================================

animation = FuncAnimation(
    fig,
    update,
    frames=101,
    interval=30,
    repeat=False,
    blit=False
)

plt.show()
