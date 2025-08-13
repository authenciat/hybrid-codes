from itertools import combinations
from pauli_methods import pauli_multiply, multiply_pauli_list


class StabilizerCode:
    # Base class for quantum error correcting codes with stabilizer generators and logical operators
    
    # Initialize a stabilizer code with n physical qubits, k logical qubits, distance d, and optional classical bits k_c
    def __init__(self, n, k, d, stabilizers, logical_x, logical_z, classical_z=None, k_c=0):
        self.n = n  # number of physical qubits
        self.k = k  # number of logical qubits
        self.k_c = k_c  # number of classical bits (for hybrid codes)
        self.d = d  # code distance
        self.stabilizers = stabilizers
        self.logical_x = logical_x
        self.logical_z = logical_z
        self.classical_z = classical_z if classical_z else {}
    
    # Return string representation in [[n,k,d]] or [[n,k:c,d]] format
    def __str__(self):
        if self.k_c > 0:
            return f"[[{self.n},{self.k}:{self.k_c},{self.d}]] Hybrid Code"
        return f"[[{self.n},{self.k},{self.d}]] Stabilizer Code"
    
    # Calculate all elements of the stabilizer group by multiplying combinations of generators
    def get_stabilizer_group(self):
        # Dictionary to store stabilizer -> list of generator indices
        stabilizer_dict = {'I' * self.n: []}  # Identity comes from empty product
        
        # Add individual generators first
        for i, gen in enumerate(self.stabilizers):
            stabilizer_dict[gen] = [i+1]
        
        # Try all combinations of generators
        for r in range(2, len(self.stabilizers) + 1):
            for combo_indices in combinations(range(len(self.stabilizers)), r):
                combo = [self.stabilizers[i] for i in combo_indices]
                product = multiply_pauli_list(combo)
                stabilizer_dict[product] = list(i+1 for i in combo_indices)
        
        return stabilizer_dict

    # Calculate all the possible logical operators for an operator by multiplying it with all the elements of the stabilizer group
    def get_logical_operators(self, operator):
        stabilizer_group = self.get_stabilizer_group()
        logical_operators = {}
        
        # Then multiply with each stabilizer and track which ones were used
        for stabilizer, indices in stabilizer_group.items():
            product = pauli_multiply(operator, stabilizer)
            if product not in logical_operators:  # Only add if we haven't seen this operator before
                logical_operators[product] = indices
        
        return logical_operators

    # Get the support of an operator, returns a tuple of qubit indices
    def get_support(self, operator):
        support = []
        for i, qubit in enumerate(operator):
            if qubit != 'I':
                support.append(i + 1)
        return tuple(sorted(support))

    # Get a set of all the supports of a logical operators
    def get_all_supports(self, operator):
        logical_operators = self.get_logical_operators(operator)
        support_to_operators = {}
        for logical_operator in logical_operators.keys():
            support = self.get_support(logical_operator)
            if support not in support_to_operators:
                support_to_operators[support] = []
            support_to_operators[support].append(logical_operator)
        return support_to_operators

    # Helper function to check if one support is a subset of another
    def is_subset(self, subset, superset):
        return all(x in superset for x in subset)

    # Get a dictionary of all subsets and which logical operators (X,Z,Y) can be implemented on them
    def get_supported_operators(self, index):
        # Get logical Y by multiplying X and Z
        logical_y = multiply_pauli_list([self.logical_x[index], self.logical_z[index]])
        
        # Get all supports for each logical operator
        x_supports = self.get_all_supports(self.logical_x[index])
        z_supports = self.get_all_supports(self.logical_z[index])
        y_supports = self.get_all_supports(logical_y)
        
        # Dictionary of subset:logical operators supported
        result = {}
        
        # Generate and process all subsets
        for size in range(0, self.n + 1):
            for subset in combinations(range(1, self.n + 1), size):
                operators = []
                
                # Check quantum operators
                if any(self.is_subset(x_support, subset) for x_support in x_supports):
                    operators.append('X' + str(index))
                if any(self.is_subset(z_support, subset) for z_support in z_supports):
                    operators.append('Z' + str(index))
                if any(self.is_subset(y_support, subset) for y_support in y_supports):
                    operators.append('Y' + str(index))
                
                # Check classical operators if they exist
                if self.classical_z:
                    z2_supports = self.get_all_supports(self.classical_z[2])
                    z3_supports = self.get_all_supports(self.classical_z[3])
                    z2z3_supports = self.get_all_supports(pauli_multiply(self.classical_z[2], self.classical_z[3]))
                    
                    if any(self.is_subset(support, subset) for support in z2_supports):
                        operators.append('Z2')
                    if any(self.is_subset(support, subset) for support in z3_supports):
                        operators.append('Z3')
                    if any(self.is_subset(support, subset) for support in z2z3_supports):
                        operators.append('Z2Z3')
                
                result[subset] = operators
        
        return result



# Define the [[4,1,2]] stabilizer code
four_one_two = StabilizerCode(
    n=4,
    k=1,
    d=2,
    stabilizers=["XXXX", "IIZZ", "ZZII"],
    logical_x={1: "XXII"},
    logical_z={1: "ZIZI"},
    k_c=1
)

# Define the [[8,1,3]] stabilizer code
eight_one_three = StabilizerCode(
    n=8,
    k=1,
    d=3,
    stabilizers=[
        "XXXXXXXX",  # S1 = X1X2X3X4X5X6X7X8
        "ZZZZZZZZ",  # S2 = Z1Z2Z3Z4Z5Z6Z7Z8
        "IXIXYZYZ",  # 
        "IXZYIXZY",  # 
        "IYXZXZIY",  # 
        "IIZZIIZZ",  # 
        "IIIIZZZZ"   # 
    ],
    logical_x={1: "XXIIIZIZ"},  # X4X5X7X8
    logical_z={1: "IZIZIZIZ"}   # Z2X3Z5X8
)

# Define the [[8,1:2,3]] hybrid stabilizer code
eight_one_two_three = StabilizerCode(
    n=8,
    k=1,
    d=3,
    stabilizers=[
        "XXXXXXXX",  # S1 = X1X2X3X4X5X6X7X8
        "ZZZZZZZZ",  # S2 = Z1Z2Z3Z4Z5Z6Z7Z8
        "IXIXYZYZ",  # 
        "IXZYIXZY",  # 
        "IYXZXZIY",  # 
    ],
    logical_x={1: "XXIIIZIZ"},  # X4X5X7X8
    logical_z={1: "IZIZIZIZ"},   # Z2X3Z5X8
    classical_z={
        2: "IIZZIIZZ",
        3: "IIIIZZZZ" 
    },
    k_c=2
)

# Define the [[8,3,3]] stabilizer code
eight_three_three = StabilizerCode(
    n=8,
    k=3,
    d=3,
    stabilizers=[
        "XXXXXXXX",  # S1 = X1X2X3X4X5X6X7X8
        "ZZZZZZZZ",  # S2 = Z1Z2Z3Z4Z5Z6Z7Z8
        "IXIXYZYZ",  # 
        "IXZYIXZY",  # 
        "IYXZXZIY",  # 
    ],
    logical_x={1: "XXIIIZIZ", 2: "XIXZIIZI", 3: "XIIZXZII"},  # X4X5X7X8
    logical_z={1: "IZIZIZIZ", 2: "IIZZIIZZ", 3: "IIIIZZZZ"},   # Z2X3Z5X8
)

# define the [[7,1,3]] stabilizer code
seven_one_three = StabilizerCode(
    n=7,
    k=1,
    d=3,
    stabilizers=[
        "IIIXXXX",  # S1 =
        "IXXIIXX",  # S2 = 
        "XIXIXIX",  # 
        "IIIZZZZ",  # 
        "IZZIIZZ",  # 
        "ZIZIZIZ"
    ],
    logical_x={1: "XXXXXXX"},  # X4X5X7X8
    logical_z={1: "ZZZZZZZ"},   # Z2X3Z5X8
)

# define the [[5,1,3]] stabilizer code
five_one_three = StabilizerCode(
    n=5,
    k=1,
    d=3,
    stabilizers=[
        "XZZXI",  # S1 =
        "IXZZX",  # S2 = 
        "XIXZZ",  # 
        "ZXIXZ"
    ],
    logical_x={1: "XXXXX"},  # X4X5X7X8
    logical_z={1: "ZZZZZ"},   # Z2X3Z5X8
)