#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt

f_input = 'collaboration-network.csv'

# Load the network
G_multi = nx.read_edgelist(f_input, delimiter=' ', create_using=nx.MultiGraph())

# Create a new graph
G = nx.Graph()
for u, v in G_multi.edges():
    if G.has_edge(u,v):
        G[u][v]['weight'] += 1
    else:
        G.add_edge(u, v, weight=1)

# Remove nodes with n hops or more to the center node
center_node = 'schochastics'
nodes_to_remove = [node for node in G.nodes() if nx.shortest_path_length(G, center_node, node) >= 2]
G.remove_nodes_from(nodes_to_remove)

# Calculate node degrees for scaling node sizes
node_sizes = [G.degree(node) * 100 for node in G.nodes()]

# Draw the network G spread
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=1)  # Seed for reproducibility
nx.draw(G, pos, with_labels=True, node_color="lightblue", font_size=10, node_size=node_sizes)
weights = nx.get_edge_attributes(G, 'weight')
#nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)
plt.title("Collaboration Network")

plt.show()
