
import math

# =====================================
# ROBOT ARM KINEMATICS INTEGRATION
# =====================================

# PART 1: FORWARD KINEMATICS

def forward_kinematics(L1, L2, theta1, theta2):

    # Convert degrees into radians
    t1 = math.radians(theta1)
    t2 = math.radians(theta2)

    # Calculate end effector position
    x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)
    y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)

    return x, y


# PART 2: INVERSE KINEMATICS

def inverse_kinematics(L1, L2, x, y):

    # Calculate target distance
    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check target reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    # Calculate elbow angle
    D = (r_squared - L1**2 - L2**2) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    angle = math.acos(D)

    # Store both elbow configurations
    elbow_solutions = [
        ("Elbow Down", angle),
        ("Elbow Up", -angle)
    ]

    results = []

    for name, theta2 in elbow_solutions:

        # Calculate shoulder angle
        k1 = L1 + L2 * math.cos(theta2)
        k2 = L2 * math.sin(theta2)

        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # Convert radians into degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        results.append((name, theta1_deg, theta2_deg))

    return results


# PART 3: MAIN PROGRAM

# Define robotic arm link lengths
L1 = 5
L2 = 7

# Define target position
target_x = 6
target_y = 5

print("ROBOT ARM KINEMATICS SYSTEM")
print("================================")

# Calculate inverse kinematics
solutions = inverse_kinematics(
    L1, L2, target_x, target_y
)

if solutions is None:

    print("Target position is unreachable!")

else:

    for name, theta1, theta2 in solutions:

        print("\n", name)

        print("Shoulder Angle:", round(theta1, 3))
        print("Elbow Angle:", round(theta2, 3))

        # Validate using forward kinematics
        actual_x, actual_y = forward_kinematics(
            L1, L2, theta1, theta2
        )

        print("Calculated X:", round(actual_x, 3))
        print("Calculated Y:", round(actual_y, 3))

        # Calculate position error
        error = math.hypot(
            target_x - actual_x,
            target_y - actual_y
        )

        print("Position Error:", error)

        if error < 0.000001:
            print("Validation: PASSED")
        else:
            print("Validation: FAILED")

        print("--------------------------------")
