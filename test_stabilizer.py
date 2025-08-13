from stabilizer_code import four_one_two, eight_one_three, eight_one_two_three, eight_three_three, seven_one_three, five_one_three
from pauli_methods import multiply_pauli_list, pauli_multiply
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

# Get all logical operators and their generating stabilizers
# logical_y = pauli_multiply(eight_one_three.logical_x[1], eight_one_three.logical_z[1])  # Get Y operator for first logical qubit
logical_z2 = eight_one_two_three.get_logical_operators(eight_one_two_three.classical_z[2])
logical_z3 = eight_one_two_three.get_logical_operators(eight_one_two_three.classical_z[3])

# print(f"Original operator: {eight_one_two_three.logical_z[2]}")
print("\nAll equivalent logical z2 operators and the stabilizer indices used to generate them:")
for operator, indices in sorted(logical_z2.items()):
        print(f"{operator}: Used stabilizers {indices}")

print("\nAll equivalent logical z3 operators and the stabilizer indices used to generate them:")
for operator, indices in sorted(logical_z3.items()):
        print(f"{operator}: Used stabilizers {indices}")

logical_z2_supports = eight_one_two_three.get_all_supports(eight_one_two_three.classical_z[2])
logical_z3_supports = eight_one_two_three.get_all_supports(eight_one_two_three.classical_z[3])

print("\nSubsets and the logical z2 operators that can be implemented on them:")
for operator, indices in sorted(logical_z2_supports.items()):
        print(f"{operator}: {indices}")

print("\nSubsets and the logical z3 operators that can be implemented on them:")
for operator, indices in sorted(logical_z3_supports.items()):
        print(f"{operator}: {indices}")

