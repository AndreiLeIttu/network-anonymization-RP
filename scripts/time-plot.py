import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

results_1 = [
    (4.4867819, 'graph_38.dzn'), (0.2072846, 'very-small-example.dzn'),
    (4.6092192, 'graph_15.dzn'), (0.3329078, 'southern-women.dzn'),
    (0.5025642, 'south-african-companies.dzn'), (0.8167647, 'aves-weaver-social1.dzn'),
    (0.3302825, 'mammalia-voles-kcs-trapping43.dzn'), (26.1369189, 'graph_6.dzn')
]

results_2 = [
    (2.9452736, 'graph_23.dzn'), (6.2906581, 'graph_1.dzn'), (1.6709923, 'graph_8.dzn'),
    (1.0409391, 'graph_7.dzn'), (0.3214559, 'graph_36.dzn'), (0.2119386, 'graph_31.dzn'),
    (0.1811103, 'mammalia-voles-kcs-trapping43.dzn'), (0.2286095, 'graph_10.dzn'),
    (35.7150501, 'mammalia_baboon-association-group17.dzn'), (3.6793649, 'graph_2.dzn'),
    (39.3774566, 'graph_20.dzn'), (3.6799897, 'graph_0.dzn'), (7.0031944, 'graph_25.dzn'),
    (4.653614, 'graph_19.dzn'), (5.0085667, 'graph_37.dzn'), (3.0847159, 'graph_39.dzn'),
    (0.6591347, 'graph_22.dzn'), (3.7287924, 'mammalia-baboon-association-group18.dzn'),
    (0.8806163, 'small-example.dzn'), (0.1905307, 'south-african-companies.dzn'),
    (0.1988536, 'southern-women.dzn'), (0.9108935, 'graph_33.dzn'),
    (0.2393786, 'graph_38.dzn'), (2.740851, 'graph_34.dzn'), (7.0781063, 'graph_12.dzn'),
    (41.4136837, 'rhesus-macaques.dzn'), (3.6051342, 'graph_16.dzn'),
    (78.6428897, 'graph_24.dzn'), (2.9405832, 'aves-weaver-social1.dzn'),
    (6.1421121, 'graph_29.dzn'), (4.0390377, 'graph_9.dzn'),
    (119.90011, 'aves-barn-swallow-non-physical.dzn'), (23.6602349, 'graph_17.dzn'),
    (0.488563, 'graph_35.dzn'), (6.0897939, 'graph_13.dzn'),
    (0.9387768, 'graph_5.dzn'), (0.1773982, 'very-small-example.dzn'),
    (0.433075, 'graph_28.dzn'), (0.2925641, 'graph_3.dzn'),
    (14.5676458, 'graph_18.dzn'), (3.5427809, 'graph_21.dzn'),
    (3.1860446, 'graph_4.dzn'), (4.7927894, 'graph_11.dzn'),
    (9.4186305, 'graph_27.dzn'), (0.6062848, 'graph_30.dzn'),
    (9.157825, 'aves-weaver-social14.dzn'), (0.2225561, 'graph_15.dzn'),
    (11.9633324, 'graph_14.dzn'), (0.2555226, 'graph_26.dzn'),
    (0.9927404, 'graph_32.dzn'), (0.2682284, 'graph_6.dzn')
]

dict1 = {name: round(time, 2) for time, name in results_1}
dict2 = {name: round(time, 2) for time, name in results_2}
all_filenames = set(dict1) | set(dict2)

TIMEOUT_CAP = 300.0
x, y, colors, markers = [], [], [], []

for name in sorted(all_filenames):
    t1 = dict1.get(name, -1)
    t2 = dict2.get(name, -1)
    capped_t1 = t1 if t1 != -1 else TIMEOUT_CAP
    capped_t2 = t2 if t2 != -1 else TIMEOUT_CAP
    x.append(capped_t1)
    y.append(capped_t2)

    if t1 == -1 and t2 == -1:
        colors.append("white")
        markers.append("x")
    elif t1 == -1:
        colors.append("white")
        markers.append("v")
    elif t2 == -1:
        colors.append("white")
        markers.append("^")
    else:
        colors.append("white")
        markers.append("o")

# Plot with dark background style
fig, ax = plt.subplots(figsize=(7, 7), facecolor='none')
ax.set_facecolor('none')

# Set white text and spines
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

ax.set_xlabel('BasicModel Running time (s)', fontsize=12, color='white')
ax.set_ylabel('IsoModel Running time (s)', fontsize=12, color='white')
ax.set_title('Running time Comparison (log-log scale)', fontsize=14, color='white')

# Log-log scale
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(0.1, TIMEOUT_CAP * 1.1)
ax.set_ylim(0.1, TIMEOUT_CAP * 1.1)

# Scatter plot
for xi, yi, ci, mi in zip(x, y, colors, markers):
    ax.scatter(xi, yi, color=ci, marker=mi, s=50, edgecolors='white', alpha=0.8)

# Diagonal
ax.plot([0.1, TIMEOUT_CAP], [0.1, TIMEOUT_CAP], linestyle='--', color='white', linewidth=1, label='y = x')

# Legend
legend_elements = [
    Line2D([0], [0], marker='o', color='none', label='Both Solved',
           markerfacecolor='white', markeredgecolor='white', markersize=8),
    Line2D([0], [0], marker='v', color='none', label='BasicModel Timeout',
           markerfacecolor='white', markeredgecolor='white', markersize=8),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8, facecolor='none', edgecolor='white', labelcolor='white')

# Grid
ax.grid(True, which="both", ls="--", linewidth=0.5, color='white', alpha=0.3)

# Save
plt.savefig("runtime_comparison_loglog_dark.png", dpi=300, transparent=True)
plt.show()
