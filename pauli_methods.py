import numpy as np
from itertools import combinations, product
import sympy as sp
from sympy import Matrix, GF


# Lookup table for single-qubit Pauli operator multiplication
PAULI_MULT = {
    ('I', 'I'): 'I', ('I', 'X'): 'X', ('I', 'Y'): 'Y', ('I', 'Z'): 'Z',
    ('X', 'I'): 'X', ('X', 'X'): 'I', ('X', 'Y'): 'Z', ('X', 'Z'): 'Y',
    ('Y', 'I'): 'Y', ('Y', 'X'): 'Z', ('Y', 'Y'): 'I', ('Y', 'Z'): 'X',
    ('Z', 'I'): 'Z', ('Z', 'X'): 'Y', ('Z', 'Y'): 'X', ('Z', 'Z'): 'I'
}


# Multiply two Pauli operators of the same length (e.g., 'IXYZ' * 'XIZY')
def pauli_multiply(P1, P2):
    if len(P1) != len(P2):
        raise ValueError("Pauli operators must have the same length")
    
    if len(P1) == 1:
        return PAULI_MULT.get((P1, P2), 'I')
    
    # Multiply each position and join the results
    result = ''
    for i in range(len(P1)):
        result += PAULI_MULT.get((P1[i], P2[i]), 'I')
    return result


# Multiply a list of Pauli operators in sequence (e.g., ['IXYZ', 'XIZY', 'IIXY'])
def multiply_pauli_list(paulis):
    if not paulis:
        raise ValueError("List of Pauli operators cannot be empty")
    
    # Start with the first operator
    result = paulis[0]
    
    # Multiply with each subsequent operator
    for i in range(1, len(paulis)):
        result = pauli_multiply(result, paulis[i])
    
    return result

