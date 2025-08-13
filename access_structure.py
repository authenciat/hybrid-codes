from stabilizer_code import four_one_two, eight_one_three, eight_one_two_three, eight_three_three, seven_one_three, five_one_three
from pauli_methods import multiply_pauli_list, pauli_multiply
import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations

# Get all supports and their supported logical operators
support_info = eight_one_two_three.get_supported_operators(1)  # for first logical qubit

all_qubits = set(range(1, 9))

# Create a graph to represent the access structure
G = nx.DiGraph()  # Using directed graph for clearer hierarchy

# Add nodes and classify them by information content
no_info_nodes = []    # 0 operators - no info (red)
partial_info_nodes = []  # 1 operator - partial info (yellow)
full_info_nodes = []   # 3 operators - full info (green)

# Add all nodes first
for subset, ops in support_info.items():
    node_name = str(subset)
    G.add_node(node_name, level=len(subset))  # Store size as level
    
    if len(ops) == 6:
        full_info_nodes.append(node_name)
    elif len(ops) == 4:
        partial_info_nodes.append(node_name)
    elif {'X1', 'Z3'}.issubset(ops) or {'Z1', 'Z2'}.issubset(ops) or {'Y1', 'Z2Z3'}.issubset(ops):
        partial_info_nodes.append(node_name)
    else:
        no_info_nodes.append(node_name)


# Add edges between adjacent levels
for size in range(len(all_qubits)):
    for subset1 in combinations(all_qubits, size):
        node1 = str(subset1)
        # Connect to supersets one level up
        for subset2 in combinations(all_qubits, size + 1):
            if all(q in subset2 for q in subset1):
                node2 = str(subset2)
                G.add_edge(node1, node2)

# Set up the plot with hierarchical layout
plt.figure(figsize=(20, 20))
pos = nx.multipartite_layout(G, subset_key="level", align='horizontal')

# Draw nodes with different colors based on information content
nx.draw_networkx_nodes(G, pos, nodelist=no_info_nodes, node_color='red', node_size=500, alpha=0.6)
nx.draw_networkx_nodes(G, pos, nodelist=partial_info_nodes, node_color='yellow', node_size=500, alpha=0.6)
nx.draw_networkx_nodes(G, pos, nodelist=full_info_nodes, node_color='green', node_size=500, alpha=0.6)

# Draw edges and labels
nx.draw_networkx_edges(G, pos, alpha=0.2, arrows=True)
nx.draw_networkx_labels(G, pos, font_size=6)

plt.title("Complete Access Structure of the Code\nRed: No Info, Yellow: Partial Info, Green: Full Info")
plt.axis('off')
plt.tight_layout()
plt.savefig('access_structure.png', dpi=300, bbox_inches='tight')
plt.close()

print("Complete access structure graph has been saved as 'access_structure.png'")

# Print detailed results
print("\nSupports and their logical operators:")
for support, operators in sorted(support_info.items()):
    print(f"qubits {support}: {', '.join(operators)}")
