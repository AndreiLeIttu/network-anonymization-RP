import numpy as np
import matplotlib.pyplot as plt

# Data for k = 2 experiments
results_k2 = [
    ("graph_4.dzn", 14, 0),
    ("graph_5.dzn", 12, 1),
    ("graph_27.dzn", 14, 2),
    ("rhesus-macaques.dzn", 16, 2),
    ("graph_22.dzn", 11, 1),
    ("graph_17.dzn", 17, 0),
    ("graph_35.dzn", 8, 3),
    ("graph_26.dzn", 9, 2),
    ("aves-weaver-social14.dzn", 11, 4),
    ("graph_39.dzn", 15, 0),
    ("graph_0.dzn", 12, 1),
    ("aves-barn-swallow-non-physical.dzn", 17, 4),
    ("graph_13.dzn", 14, 3),
    ("graph_2.dzn", 9, 2),
    ("graph_30.dzn", 11, 1),
    ("mammalia-baboon-association-group18.dzn", 10, 3),
    ("graph_3.dzn", 10, 0),
    ("graph_33.dzn", 11, 1),
    ("graph_24.dzn", 15, 2),
    ("graph_12.dzn", 14, 1),
    ("graph_38.dzn", 8, 2),
    ("graph_6.dzn", 9, 1),
    ("graph_8.dzn", 10, 2),
    ("graph_16.dzn", 11, 3),
    ("graph_31.dzn", 8, 1),
    ("small-example.dzn", 8, 2),
    ("graph_29.dzn", 12, 3),
    ("graph_15.dzn", 8, 1),
    ("graph_19.dzn", 15, 0),
    ("graph_18.dzn", 15, 0),
    ("graph_14.dzn", 12, 3),
    ("graph_28.dzn", 11, 1),
    ("graph_32.dzn", 8, 1),
    ("graph_23.dzn", 9, 2),
    ("graph_36.dzn", 11, 1),
    ("graph_11.dzn", 12, 3),
    ("graph_34.dzn", 13, 1),
    ("graph_37.dzn", 12, 2),
    ("aves-weaver-social1.dzn", 7, 3),
    ("graph_7.dzn", 12, 1),
    ("mammalia_baboon-association-group17.dzn", 9, 3),
    ("south-african-companies.dzn", 6, 1),
    ("graph_21.dzn", 11, 1),
    ("graph_10.dzn", 9, 1),
    ("graph_20.dzn", 17, 0),
    ("graph_9.dzn", 13, 3),
    ("graph_25.dzn", 14, 2),
    ("graph_1.dzn", 12, 4),
]

# Data for k = 4 experiments
results_k4 = [
    ("graph_17.dzn", 17, 1),
    ("graph_32.dzn", 8, 6),
    ("graph_24.dzn", 15, 4),
    ("graph_31.dzn", 8, 1),
    ("mammalia_baboon-association-group17.dzn", None, None),
    ("graph_12.dzn", 14, 3),
    ("graph_27.dzn", 14, 5),
    ("graph_19.dzn", None, None),
    ("small-example.dzn", 8, 3),
    ("very-small-example.dzn", 3, 1),
    ("south-african-companies.dzn", 6, 4),
    ("graph_3.dzn", 10, 5),
    ("graph_23.dzn", 9, 3),
    ("graph_29.dzn", 12, 5),
    ("graph_34.dzn", 13, 2),
    ("graph_16.dzn", 11, 6),
    ("aves-weaver-social1.dzn", 7, 9),
    ("graph_4.dzn", 14, 2),
    ("graph_18.dzn", 15, 1),
    ("graph_6.dzn", 9, 1),
    ("graph_14.dzn", 12, 6),
    ("graph_11.dzn", 12, 6),
    ("graph_0.dzn", 12, 3),
    ("graph_30.dzn", 11, 3),
    ("graph_13.dzn", 14, 5),
    ("graph_2.dzn", 9, 3),
    ("graph_25.dzn", 14, 4),
    ("graph_26.dzn", 9, 4),
    ("graph_7.dzn", 12, 1),
    ("graph_33.dzn", 11, 5),
    ("graph_22.dzn", 11, 5),
    ("graph_38.dzn", 8, 5),
    ("graph_8.dzn", 10, 6),
    ("graph_9.dzn", 13, 5),
    ("graph_35.dzn", 8, 5),
    ("rhesus-macaques.dzn", None, None),
    ("graph_28.dzn", 11, 1),
    ("graph_36.dzn", 11, 1),
    ("graph_39.dzn", 15, 2),
    ("graph_10.dzn", 9, 2),
    ("aves-barn-swallow-non-physical.dzn", None, None),
    ("aves-weaver-social14.dzn", 11, 8),
    ("graph_15.dzn", 8, 2),
    ("graph_21.dzn", 11, 1),
    ("graph_1.dzn", 12, 7),
    ("graph_20.dzn", 17, 0),
    ("graph_37.dzn", 12, 4),
    ("graph_5.dzn", 12, 4),
    ("mammalia-baboon-association-group18.dzn", 10, 6),
]

# Placeholder for k = 6 experiments (to be filled later)
results_k6 = [
    ("graph_16.dzn", None, None),
    ("south-african-companies.dzn", 6, 4),
    ("graph_8.dzn", 10, 12),
    ("mammalia_baboon-association-group17.dzn", None, None),
    ("aves-weaver-social1.dzn", 7, 9),
    ("rhesus-macaques.dzn", None, None),
    ("graph_15.dzn", 8, 6),
    ("graph_14.dzn", None, None),
    ("graph_2.dzn", 9, 3),
    ("graph_33.dzn", 11, 8),
    ("graph_27.dzn", None, None),
    ("graph_18.dzn", None, None),
    ("graph_38.dzn", 8, 7),
    ("graph_34.dzn", 13, 2),
    ("graph_37.dzn", 12, 7),
    ("graph_10.dzn", 9, 4),
    ("graph_23.dzn", 9, 5),
    ("graph_31.dzn", 8, 3),
    ("graph_1.dzn", None, None),
    ("graph_12.dzn", None, None),
    ("graph_26.dzn", 9, 6),
    ("small-example.dzn", None, None),
    ("graph_24.dzn", None, None),
    ("aves-barn-swallow-non-physical.dzn", None, None),
    ("graph_0.dzn", 12, 4),
    ("graph_21.dzn", 11, 3),
    ("graph_28.dzn", 11, 4),
    ("graph_30.dzn", 11, 6),
    ("graph_19.dzn", None, None),
    ("graph_7.dzn", 12, 3),
    ("graph_4.dzn", 14, 3),
    ("graph_5.dzn", 12, 5),
    ("graph_3.dzn", 10, 5),
    ("mammalia-baboon-association-group18.dzn", None, None),
    ("graph_6.dzn", 9, 6),
    ("graph_35.dzn", 8, 7),
    ("aves-weaver-social14.dzn", None, None),
    ("graph_39.dzn", 15, 2),
    ("graph_29.dzn", None, None),
    ("graph_36.dzn", 11, 3),
    ("graph_17.dzn", 17, 3),
    ("graph_11.dzn", None, None),
    ("graph_25.dzn", None, None),
    ("graph_9.dzn", None, None),
    ("graph_20.dzn", None, None),
    ("graph_32.dzn", 8, 8),
    ("graph_13.dzn", None, None),
    ("graph_22.dzn", 11, 9),
]

# Convert to dictionaries
dict_k2 = {f: (n, e) for f, n, e in results_k2}
dict_k4 = {f: (n, e) for f, n, e in results_k4}
dict_k6 = {f: (n, e) for f, n, e in results_k6}

# Collect only filenames present in all three
common_keys = set(dict_k2) & set(dict_k4) & set(dict_k6)

# Filter strictly: all node and edge values must be non-None and node counts must match
aligned_data = []
for f in common_keys:
    n2, e2 = dict_k2[f]
    n4, e4 = dict_k4[f]
    n6, e6 = dict_k6[f]
    if None not in (n2, e2, n4, e4, n6, e6) and n2 == n4 == n6:
        aligned_data.append((n2, e2, e4, e6))

# Sort by number of nodes
aligned_data.sort(key=lambda x: x[0])

# Extract for plotting
nodes = [n for n, _, _, _ in aligned_data]
edges_k2 = [e2 for _, e2, _, _ in aligned_data]
edges_k4 = [e4 for _, _, e4, _ in aligned_data]
edges_k6 = [e6 for _, _, _, e6 in aligned_data]

# Plot
plt.style.use('grayscale')
plt.figure(figsize=(4, 3))

plt.plot(nodes, edges_k2, linestyle='--', marker='x', label='k = 2')
plt.plot(nodes, edges_k4, linestyle='-', marker='s', label='k = 4')
plt.plot(nodes, edges_k6, linestyle=':', marker='o', label='k = 6')

plt.xlabel('Number of Vertices', fontsize=10)
plt.ylabel('Number of dummy edges', fontsize=10)
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.legend(fontsize=8, loc='best', frameon=False)
plt.grid(False)
plt.tight_layout()

plt.savefig("gaga_filtered_plot.png", dpi=300)
plt.show()