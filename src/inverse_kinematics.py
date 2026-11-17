
import math

def inverse_kinematics(L1, L2, x, y):

    # Calculate target distance
    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        print("Target position is unreachable!")
        return None

    # Calculate D
    D = (r_squared - L1**2 - L2**2) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    # Calculate both elbow solutions
    elbow_down = math.acos(D)
    elbow_up = -math.acos(D)

    solutions = []

    # Calculate shoulder angle for both solutions
    for theta2 in [elbow_down, elbow_up]:

        k1 = L1 + L2 * math.cos(theta2)
        k2 = L2 * math.sin(theta2)

        theta1 = math.atan2(y, x) - math.atan2(k2, k1)

        # Convert radians to degrees
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        solutions.append((theta1_deg, theta2_deg))

    return solutions


# Main program
L1 = 5
L2 = 7

target_x = 6
target_y = 5

results = inverse_kinematics(L1, L2, target_x, target_y)

if results is not None:

    print("ROBOTIC ARM INVERSE KINEMATICS")
    print("--------------------------------")
    print("Target X:", target_x)
    print("Target Y:", target_y)

    print("\nELBOW DOWN SOLUTION")
    print("Shoulder:", round(results[0][0], 3))
    print("Elbow:", round(results[0][1], 3))

    print("\nELBOW UP SOLUTION")
    print("Shoulder:", round(results[1][0], 3))
    print("Elbow:", round(results[1][1], 3))
