
import csv
import math

# Robot configuration
L1 = 5
L2 = 7

# Test positions
targets = [
    (6, 5),
    (4, 8),
    (5, 5),
    (10, 2),
    (20, 15),
    (0, 0)
]

configurations = ["up", "down"]

# Inverse Kinematics
def inverse_kinematics(x, y, choice):

    distance = math.hypot(x, y)

    if distance > L1 + L2 or distance < abs(L1 - L2):
        return None

    D = (
        x**2 + y**2 - L1**2 - L2**2
    ) / (2 * L1 * L2)

    D = max(-1.0, min(1.0, D))

    theta2 = math.acos(D)

    if choice == "up":
        theta2 = -theta2

    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)

    theta1 = math.atan2(y, x) - math.atan2(k2, k1)

    return math.degrees(theta1), math.degrees(theta2)


# Forward Kinematics
def forward_kinematics(theta1, theta2):

    t1 = math.radians(theta1)
    t2 = math.radians(theta2)

    x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)
    y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)

    return x, y


# Store testing results
results = []

passed = 0
failed = 0
unreachable = 0

# Run all tests
for x, y in targets:

    for choice in configurations:

        solution = inverse_kinematics(x, y, choice)

        if solution is None:

            status = "UNREACHABLE"
            shoulder = ""
            elbow = ""
            error = ""

            unreachable += 1

        else:

            shoulder, elbow = solution

            actual_x, actual_y = forward_kinematics(
                shoulder, elbow
            )

            error = math.hypot(
                x - actual_x,
                y - actual_y
            )

            if error < 0.000001:
                status = "PASSED"
                passed += 1
            else:
                status = "FAILED"
                failed += 1

        results.append([
            x,
            y,
            choice,
            shoulder,
            elbow,
            error,
            status
        ])


# Generate CSV report
with open(
    "robot_testing_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Target X",
        "Target Y",
        "Configuration",
        "Shoulder Angle",
        "Elbow Angle",
        "Position Error",
        "Status"
    ])

    writer.writerows(results)


# Display summary
print("ROBOT TESTING REPORT GENERATED")
print("--------------------------------")

print("Total Tests:", len(results))
print("Passed:", passed)
print("Failed:", failed)
print("Unreachable:", unreachable)

print("\nCSV file created successfully!")
