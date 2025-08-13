"""
Analysis of logical operators for the [[8,3,3]] stabilizer code.
This script finds all 4^3=64 logical operators and their minimum weights
when multiplied by stabilizer elements.
"""

from stabilizer_code import eight_three_three
from itertools import product
from pauli_methods import pauli_multiply
import collections

def get_weight(pauli_string):
    """Return the weight of a Pauli string (number of non-identity elements)."""
    return sum(1 for p in pauli_string if p != 'I')

# Build map from logical to full 8-qubit strings
logical_map = {}

for i in range(1, 4):  # logical qubits 1,2,3
    logical_map[(i, 'I')] = 'I' * eight_three_three.n
    logical_map[(i, 'X')] = eight_three_three.logical_x[i]
    logical_map[(i, 'Z')] = eight_three_three.logical_z[i]
    # Y = X*Z (Pauli multiply)
    logical_map[(i, 'Y')] = pauli_multiply(
        eight_three_three.logical_x[i],
        eight_three_three.logical_z[i]
    )

# Now analyze each logical 3-qubit operator
symbols = ['I', 'X', 'Y', 'Z']
length = 3
op_weights = {}
weight_distribution = collections.defaultdict(list)

print("\nAnalyzing all 4^3 = 64 logical operators...\n")

for logical_op in product(symbols, repeat=length):
    # Convert tuple to string for display
    op_str = ''.join(logical_op)
    
    # Compute the full 8-qubit operator
    full_op = 'I' * eight_three_three.n
    for i, sym in enumerate(logical_op, start=1):
        full_op = pauli_multiply(full_op, logical_map[(i, sym)])
    
    # Get all equivalent operators and find minimum weight one
    equivalent_ops = eight_three_three.get_logical_operators(full_op)
    min_weight_op = min(equivalent_ops, key=lambda x: len(eight_three_three.get_support(x)))
    min_weight = len(eight_three_three.get_support(min_weight_op))
    
    # Store results
    op_weights[op_str] = min_weight_op
    weight_distribution[min_weight].append(op_str)

# Print analysis
print("Minimum Weight Distribution:")
print("-" * 50)
for weight in sorted(weight_distribution.keys()):
    ops = weight_distribution[weight]
    print(f"\nWeight {weight} ({len(ops)} operators):")
    # Print operators in rows of 4
    for i in range(0, len(ops), 4):
        row = ops[i:i+4]
        print("  " + "  ".join(f"{op:<3}" for op in row))

print("\nDetailed Analysis:")
print("-" * 50)
for op_str, min_weight_op in sorted(op_weights.items()):
    weight = len(eight_three_three.get_support(min_weight_op))
    print(f"Logical: {op_str:<3} -> Min weight: {weight:2d} | Representative: {min_weight_op}")

