
import math
import matplotlib.pyplot as plt

# Robot link lengths
L1 = 5
L2 = 7

# Joint limits
SHOULDER_MIN = -90
SHOULDER_MAX = 180

ELBOW_MIN = -120
ELBOW_MAX = 120


# Inverse Kinematics Function
def inverse_kinematics(x, y, elbow_choice):

    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check theoretical reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    D = (
        r_squared - L1**2 - L2**2
    ) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    theta2 = math.acos(D)

    if elbow_choice == "up":
        theta2 = -theta2

    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)

    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    return math.degrees(theta1), math.degrees(theta2)


# Check whether a position is reachable
def is_reachable(x, y):

    for choice in ["up", "down"]:

        result = inverse_kinematics(x, y, choice)

        if result is None:
            continue

        shoulder, elbow = result

        shoulder_ok = (
            SHOULDER_MIN <= shoulder <= SHOULDER_MAX
        )

        elbow_ok = (
            ELBOW_MIN <= elbow <= ELBOW_MAX
        )

        if shoulder_ok and elbow_ok:
            return True

    return False


# Create coordinate points
reachable_x = []
reachable_y = []

unreachable_x = []
unreachable_y = []

# Test workspace positions
for x in range(-12, 13):
    for y in range(-12, 13):

        if is_reachable(x, y):

            reachable_x.append(x)
            reachable_y.append(y)

        else:

            unreachable_x.append(x)
            unreachable_y.append(y)


# Calculate theoretical workspace
maximum_reach = L1 + L2
minimum_reach = abs(L1 - L2)

print("ROBOT WORKSPACE ANALYSIS")
print("------------------------")

print("Maximum reach:", maximum_reach)
print("Minimum reach:", minimum_reach)

print("Reachable points:", len(reachable_x))
print("Unreachable points:", len(unreachable_x))


# Draw workspace graph
fig, ax = plt.subplots(figsize=(9, 8))

ax.scatter(
    unreachable_x,
    unreachable_y,
    color="lightgray",
    label="Unreachable",
    s=15
)

ax.scatter(
    reachable_x,
    reachable_y,
    color="green",
    label="Reachable",
    s=25
)

# Draw robot base
ax.scatter(0, 0, color="blue", s=100, label="Robot Base")

# Draw theoretical workspace circles
outer_circle = plt.Circle(
    (0, 0),
    maximum_reach,
    fill=False,
    linestyle="--",
    label="Maximum Reach"
)

inner_circle = plt.Circle(
    (0, 0),
    minimum_reach,
    fill=False,
    linestyle=":",
    label="Minimum Reach"
)

ax.add_patch(outer_circle)
ax.add_patch(inner_circle)

ax.set_title("Robotic Arm Workspace Analysis")
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")

ax.set_xlim(-13, 13)
ax.set_ylim(-13, 13)

ax.set_aspect("equal")
ax.grid(True)
ax.legend()

plt.show()
