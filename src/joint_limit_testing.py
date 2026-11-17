
import math

# Robot link lengths
L1 = 5
L2 = 7

# Joint limits in degrees
SHOULDER_MIN = -90
SHOULDER_MAX = 180

ELBOW_MIN = -120
ELBOW_MAX = 120


# Inverse Kinematics Function
def inverse_kinematics(x, y, elbow_choice):

    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check workspace reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    D = (
        r_squared - L1**2 - L2**2
    ) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    # Calculate elbow angle
    theta2 = math.acos(D)

    if elbow_choice == "up":
        theta2 = -theta2

    # Calculate shoulder angle
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)

    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    # Convert radians to degrees
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)

    return theta1, theta2


# Joint Limit Checking Function
def check_joint_limits(theta1, theta2):

    shoulder_ok = (
        SHOULDER_MIN <= theta1 <= SHOULDER_MAX
    )

    elbow_ok = (
        ELBOW_MIN <= theta2 <= ELBOW_MAX
    )

    return shoulder_ok, elbow_ok


# Main Program
target_x = 5
target_y = 5

choice = "up"

result = inverse_kinematics(
    target_x, target_y, choice
)

print("ROBOT JOINT LIMIT TESTING")
print("-------------------------")

if result is None:

    print("Target is unreachable!")

else:

    theta1, theta2 = result

    print("Target X:", target_x)
    print("Target Y:", target_y)

    print("Shoulder Angle:", round(theta1, 3))
    print("Elbow Angle:", round(theta2, 3))

    shoulder_ok, elbow_ok = check_joint_limits(
        theta1, theta2
    )

    print("\nJOINT LIMIT RESULTS")

    if shoulder_ok:
        print("Shoulder: Within limits")
    else:
        print("Shoulder: Limit exceeded")

    if elbow_ok:
        print("Elbow: Within limits")
    else:
        print("Elbow: Limit exceeded")

    if shoulder_ok and elbow_ok:
        print("\nRobot movement: ALLOWED")
    else:
        print("\nRobot movement: NOT ALLOWED")
