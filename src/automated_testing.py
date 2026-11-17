
import math

# =====================================
# PART 1: ROBOT CONFIGURATION
# =====================================

L1 = 5
L2 = 7

# Joint limits
SHOULDER_MIN = -90
SHOULDER_MAX = 180

ELBOW_MIN = -120
ELBOW_MAX = 120


# =====================================
# PART 2: FORWARD KINEMATICS
# =====================================

def forward_kinematics(theta1, theta2):

    t1 = math.radians(theta1)
    t2 = math.radians(theta2)

    x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)

    y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)

    return x, y


# =====================================
# PART 3: INVERSE KINEMATICS
# =====================================

def inverse_kinematics(x, y, choice):

    r_squared = x**2 + y**2
    distance = math.sqrt(r_squared)

    # Check reachability
    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    D = (
        r_squared - L1**2 - L2**2
    ) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    theta2 = math.acos(D)

    if choice == "up":
        theta2 = -theta2

    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)

    theta1 = (
        math.atan2(y, x)
        - math.atan2(k2, k1)
    )

    return math.degrees(theta1), math.degrees(theta2)


# =====================================
# PART 4: AUTOMATED TESTING
# =====================================

targets = [
    (6, 5),
    (4, 8),
    (5, 5),
    (10, 2),
    (20, 15),
    (0, 0)
]

configurations = ["up", "down"]

total_tests = 0
passed_tests = 0
failed_tests = 0


print("ROBOTIC ARM AUTOMATED TESTING")
print("================================")

for x, y in targets:

    for choice in configurations:

        total_tests += 1

        print("\n----------------------------")
        print("Target:", x, y)
        print("Configuration:", choice)

        result = inverse_kinematics(x, y, choice)

        if result is None:

            print("Result: UNREACHABLE")
            continue

        theta1, theta2 = result

        print("Shoulder:", round(theta1, 3))
        print("Elbow:", round(theta2, 3))

        # Check joint limits
        shoulder_ok = (
            SHOULDER_MIN <= theta1 <= SHOULDER_MAX
        )

        elbow_ok = (
            ELBOW_MIN <= theta2 <= ELBOW_MAX
        )

        if not shoulder_ok or not elbow_ok:

            print("Result: JOINT LIMIT EXCEEDED")
            failed_tests += 1
            continue

        # Validate using forward kinematics
        actual_x, actual_y = forward_kinematics(
            theta1, theta2
        )

        # Calculate position error
        error = math.hypot(
            x - actual_x,
            y - actual_y
        )

        print("Actual X:", round(actual_x, 5))
        print("Actual Y:", round(actual_y, 5))
        print("Position Error:", error)

        if error < 0.000001:

            print("TEST: PASSED")
            passed_tests += 1

        else:

            print("TEST: FAILED")
            failed_tests += 1


# =====================================
# PART 5: FINAL TEST SUMMARY
# =====================================

print("\n================================")
print("FINAL TEST SUMMARY")
print("================================")

print("Total Tests:", total_tests)
print("Passed Tests:", passed_tests)
print("Failed Tests:", failed_tests)

print("Unreachable targets are reported separately.")

if failed_tests == 0:
    print("OVERALL RESULT: SUCCESS")
else:
    print("OVERALL RESULT: CHECK FAILED TESTS")
