import networkx as nx
import matplotlib.pyplot as plt

# Create the graph
G = nx.Graph()
G.add_edges_from([
    ("Ann", "Sam"),
    ("Bob", "Sam"),
    ("Max", "Sam"),
    ("Ann", "Bob")
])

# Node positions
pos = {
    "Sam": (1, 1.5),
    "Ann": (0, 0),
    "Bob": (2, 0),
    "Max": (3, 1.5)
}

# Setup figure
fig, ax = plt.subplots(figsize=(6, 5), facecolor='none')
ax.set_facecolor('none')
ax.axis('off')
ax.margins(0.15)  # Add padding to avoid clipping

# Draw nodes (white border, no fill)
nx.draw_networkx_nodes(
    G, pos,
    node_color='none',
    edgecolors='white',
    linewidths=2,
    node_size=2000
)

# Draw edges avoiding node centers
nx.draw_networkx_edges(
    G, pos,
    edge_color='white',
    width=2,
    connectionstyle='arc3,rad=0.0'
)

# Draw white labels
nx.draw_networkx_labels(
    G, pos,
    font_color='white',
    font_size=12,
    font_weight='bold'
)

# Save the result
plt.savefig("clean_graph_no_clipping.png", dpi=300, transparent=True)
plt.close()
