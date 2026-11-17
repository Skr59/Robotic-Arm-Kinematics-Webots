
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =====================================
# PART 1: ROBOT CONFIGURATION
# =====================================

L1 = 5
L2 = 7

# =====================================
# PART 2: USER INPUT
# =====================================

print("INTERACTIVE ROBOTIC ARM SIMULATOR")
print("----------------------------------")

try:
    target_x = float(input("Enter Target X: "))
    target_y = float(input("Enter Target Y: "))

    choice = input("Choose Elbow (up/down): ").lower().strip()

except ValueError:
    print("Please enter valid numerical coordinates!")
    raise SystemExit

if choice not in ["up", "down"]:
    print("Invalid elbow choice! Enter up or down.")
    raise SystemExit

# =====================================
# PART 3: INVERSE KINEMATICS
# =====================================

def inverse_kinematics(L1, L2, x, y, choice):

    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    D = (
        r_squared - L1**2 - L2**2
    ) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    # Select elbow configuration
    if choice == "down":
        theta2 = math.acos(D)
    else:
        theta2 = -math.acos(D)

    # Calculate shoulder angle
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)

    theta1 = (
        math.atan2(y, x)
        - math.atan2(k2, k1)
    )

    return theta1, theta2


# =====================================
# PART 4: GET JOINT ANGLES
# =====================================

result = inverse_kinematics(
    L1, L2, target_x, target_y, choice
)

if result is None:

    print("Target position is unreachable!")

    raise SystemExit

theta1_target, theta2_target = result

print("\nTARGET SOLUTION")
print("----------------")
print("Shoulder:", round(math.degrees(theta1_target), 3))
print("Elbow:", round(math.degrees(theta2_target), 3))

# =====================================
# PART 5: CREATE SIMULATION
# =====================================

fig, ax = plt.subplots(figsize=(8, 7))

ax.set_title("Interactive Robotic Arm Simulator")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

ax.set_xlim(-13, 13)
ax.set_ylim(-13, 13)

ax.set_aspect("equal")
ax.grid(True)

ax.axhline(0)
ax.axvline(0)

# Show target
ax.plot(
    target_x, target_y,
    "g*", markersize=15,
    label="Target"
)

# Create links
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

ax.legend()

# =====================================
# PART 6: ANIMATION
# =====================================

def update(frame):

    alpha = frame / 100

    # Gradually move joints
    t1 = alpha * theta1_target
    t2 = alpha * theta2_target

    # Forward Kinematics
    x1 = L1 * math.cos(t1)
    y1 = L1 * math.sin(t1)

    x2 = x1 + L2 * math.cos(t1 + t2)
    y2 = y1 + L2 * math.sin(t1 + t2)

    # Update links
    link1.set_data([0, x1], [0, y1])
    link2.set_data([x1, x2], [y1, y2])

    return link1, link2


# =====================================
# PART 7: RUN ANIMATION
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

# =====================================
# PART 8: VALIDATE FINAL POSITION
# =====================================

actual_x = (
    L1 * math.cos(theta1_target)
    + L2 * math.cos(theta1_target + theta2_target)
)

actual_y = (
    L1 * math.sin(theta1_target)
    + L2 * math.sin(theta1_target + theta2_target)
)

error = math.hypot(
    target_x - actual_x,
    target_y - actual_y
)

print("\nFINAL VALIDATION")
print("----------------")
print("Target X:", target_x)
print("Actual X:", round(actual_x, 5))

print("Target Y:", target_y)
print("Actual Y:", round(actual_y, 5))

print("Position Error:", error)

if error < 0.000001:
    print("VALIDATION: PASSED")
else:
    print("VALIDATION: FAILED")
