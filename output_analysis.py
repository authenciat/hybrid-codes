from itertools import combinations, product

def commute_check(op1, op2):
    """Check if two Pauli operators commute"""
    if len(op1) != len(op2):
        raise ValueError("Operators must be same length")
    
    # Count number of positions where one operator is X/Y and other is Y/Z
    anticommuting_positions = 0
    for p1, p2 in zip(op1, op2):
        # Two operators anticommute at a position if:
        # - One is X and other is Z
        # - One is Y and other is X or Z
        if (p1 in 'XY' and p2 == 'Z') or (p1 == 'Z' and p2 in 'XY') or \
           (p1 == 'Y' and p2 == 'X') or (p1 == 'X' and p2 == 'Y'):
            anticommuting_positions += 1
    
    # Operators commute if they anticommute at an even number of positions
    return anticommuting_positions % 2 == 0

def get_support_pattern(op):
    """Get the positions and types of non-identity operators"""
    return [(i, p) for i, p in enumerate(op) if p != 'I']

def get_weight(op):
    """Get the weight of an operator (number of non-identity terms)"""
    return sum(1 for p in op if p != 'I')

def are_independent(op1, op2, logical_ops):
    """
    Check if operators are truly independent (not products of each other or logical ops)
    Returns True if operators are independent, False otherwise
    """
    # If they're identical or one is in logical_ops, they're not independent
    if op1 == op2 or op1 in logical_ops or op2 in logical_ops:
        return False
    
    # Get support patterns
    op1_support = get_support_pattern(op1)
    op2_support = get_support_pattern(op2)
    
    # Check if they have completely overlapping support
    op1_positions = {pos for pos, _ in op1_support}
    op2_positions = {pos for pos, _ in op2_support}
    if op1_positions == op2_positions:
        return False
    
    # Check if one support is contained within the other
    if op1_positions.issubset(op2_positions) or op2_positions.issubset(op1_positions):
        return False
    
    return True

# Define our logical operators
X1 = "XII"  # Weight 4 operator we want to use as X1
Y1 = "YII"  # Weight 4 operator we want to use as Y1
Z1 = "ZII"  # Weight 4 operator we want to use as Z1
logical_ops = [X1, Y1, Z1]

# Get all weight 3 and 4 operators
weight_3_ops = ["IIY", "IXY", "IYI", "IYX", "IYZ", "IZY", "XIY", "XXY", 
                "XYI", "XYX", "XYZ", "XZY", "YII", "YIX", "YIZ", "YXI", 
                "YXX", "YXZ", "YYY", "YZI", "YZX", "YZZ", "ZIY", "ZXY", 
                "ZYI", "ZYX", "ZYZ", "ZZY"]

weight_4_ops = ["IIX", "IIZ", "IXI", "IXX", "IXZ", "IYY", "IZI", "IZX", 
                "IZZ", "XII", "XIX", "XIZ", "XXI", "XXX", "XXZ", "XYY", 
                "XZI", "XZX", "XZZ", "YIY", "YXY", "YYI", "YYX", "YYZ", 
                "YZY", "ZII", "ZIX", "ZIZ", "ZXI", "ZXX", "ZXZ", "ZYY", 
                "ZZI", "ZZX", "ZZZ"]

all_ops = weight_3_ops + weight_4_ops

# First find all operators that commute with our logical operators
commuting_ops = []
for op in all_ops:
    if all(commute_check(op, log_op) for log_op in logical_ops):
        commuting_ops.append(op)

print("Analysis of potential stabilizer generators Sa and Sb:")
print("Logical operators chosen:")
print(f"X1 = {X1}")
print(f"Y1 = {Y1}")
print(f"Z1 = {Z1}")

print("\nOperators that commute with all logical operators:")
for op in commuting_ops:
    print(f"\n{op} (weight {get_weight(op)})")
    print(f"Support: {get_support_pattern(op)}")

print("\nTrying to find independent pairs among these operators...")

# Find all pairs of operators that could be Sa and Sb
valid_pairs = []
for sa, sb in combinations(commuting_ops, 2):
    # Check if operators are independent
    if not are_independent(sa, sb, logical_ops):
        continue
        
    # They already commute with logical ops, just check if they commute with each other
    if commute_check(sa, sb):
        valid_pairs.append((sa, sb))

print("\nValid pairs of truly independent stabilizer generators:")
for sa, sb in valid_pairs:
    print(f"\nSa = {sa} (weight {get_weight(sa)})")
    print(f"Support of Sa: {get_support_pattern(sa)}")
    print(f"Sb = {sb} (weight {get_weight(sb)})")
    print(f"Support of Sb: {get_support_pattern(sb)}")