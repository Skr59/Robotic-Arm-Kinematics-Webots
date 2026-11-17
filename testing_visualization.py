
import csv
import matplotlib.pyplot as plt

# ==================================
# PART 1: READ CSV FILE
# ==================================

statuses = []
errors = []
labels = []

with open("robot_testing_results.csv", "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        statuses.append(row["Status"])

        if row["Status"] == "PASSED":

            errors.append(float(row["Position Error"]))

            labels.append(
                f'({row["Target X"]}, {row["Target Y"]})'
                + " " + row["Configuration"]
            )


# ==================================
# PART 2: COUNT TEST RESULTS
# ==================================

passed = statuses.count("PASSED")
failed = statuses.count("FAILED")
unreachable = statuses.count("UNREACHABLE")

print("ROBOT TESTING VISUALIZATION")
print("---------------------------")

print("Passed:", passed)
print("Failed:", failed)
print("Unreachable:", unreachable)


# ==================================
# PART 3: TESTING SUMMARY GRAPH
# ==================================

categories = ["Passed", "Failed", "Unreachable"]

counts = [passed, failed, unreachable]

plt.figure(figsize=(8, 5))

plt.bar(categories, counts)

plt.title("Robotic Arm Testing Summary")
plt.xlabel("Test Status")
plt.ylabel("Number of Tests")

plt.grid(axis="y")

plt.savefig("testing_summary.png")

plt.show()


# ==================================
# PART 4: POSITION ERROR GRAPH
# ==================================

plt.figure(figsize=(11, 5))

plt.bar(labels, errors)

plt.title("Robotic Arm Position Error Analysis")
plt.xlabel("Target Position and Configuration")
plt.ylabel("Position Error")

plt.xticks(rotation=45, ha="right")

plt.ticklabel_format(
    axis="y",
    style="sci",
    scilimits=(0, 0)
)

plt.grid(axis="y")

plt.tight_layout()

plt.savefig("position_error.png")

plt.show()


# ==================================
# PART 5: FINAL MESSAGE
# ==================================

print("\nVISUALIZATION COMPLETED")

print("Generated files:")
print("1. testing_summary.png")
print("2. position_error.png")
