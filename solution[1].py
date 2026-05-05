# ============================================================
# Music Festival Equipment Logistics - Shortest Path Optimizer
# MIS Network Optimization Project
# ============================================================
# This script models a music festival's equipment distribution
# network. Nodes represent key locations (depots, stages, hubs),
# and edges represent transport routes with travel time (minutes)
# as weights. We use Dijkstra's algorithm (via NetworkX) to find
# the shortest (fastest) path from the Main Depot to every stage.
# ============================================================

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── 1. Load Data ─────────────────────────────────────────────
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'network_data.csv')
df = pd.read_csv(data_path)

print("=" * 60)
print("  MUSIC FESTIVAL EQUIPMENT LOGISTICS - NETWORK OPTIMIZER")
print("=" * 60)
print("\n📦 Loaded network data:")
print(df.to_string(index=False))

# ── 2. Build the Graph ────────────────────────────────────────
# We create an undirected weighted graph.
# Nodes  → festival locations (depot, stages, hubs, storage)
# Edges  → transport routes between locations
# Weight → travel_time_minutes (the cost we want to minimize)

G = nx.Graph()

for _, row in df.iterrows():
    G.add_edge(
        row['source'],
        row['target'],
        weight=row['travel_time_minutes'],
        distance=row['distance_km'],
        road_type=row['road_type']
    )

print(f"\n📊 Graph Summary:")
print(f"   • Number of nodes : {G.number_of_nodes()}")
print(f"   • Number of edges : {G.number_of_edges()}")
print(f"   • Nodes           : {list(G.nodes())}")

# ── 3. Shortest Path Analysis (Dijkstra) ─────────────────────
# The Main Depot is where all equipment originates.
# We find the shortest (fastest) path from Main_Depot to each stage.

source_node = 'Main_Depot'
target_stages = ['Stage_A', 'Stage_B', 'Stage_C']

print(f"\n🗺️  Shortest Paths from '{source_node}' to each stage:")
print("-" * 60)

results = {}
for target in target_stages:
    path = nx.dijkstra_path(G, source=source_node, target=target, weight='weight')
    length = nx.dijkstra_path_length(G, source=source_node, target=target, weight='weight')
    results[target] = {'path': path, 'time': length}
    print(f"\n   🎯 To {target}:")
    print(f"      Route     : {' → '.join(path)}")
    print(f"      Total Time: {length} minutes")

# ── 4. All-Pairs Shortest Paths ───────────────────────────────
print("\n" + "=" * 60)
print("  ALL-PAIRS SHORTEST PATH MATRIX (travel time in minutes)")
print("=" * 60)
all_nodes = list(G.nodes())
matrix = {}
for n in all_nodes:
    matrix[n] = {}
    for m in all_nodes:
        try:
            matrix[n][m] = nx.dijkstra_path_length(G, n, m, weight='weight')
        except nx.NetworkXNoPath:
            matrix[n][m] = float('inf')

matrix_df = pd.DataFrame(matrix).round(1)
print(matrix_df.to_string())

# ── 5. Network Visualization ──────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
fig.patch.set_facecolor('#1a1a2e')

# --- Color scheme ---
node_colors_map = {
    'Main_Depot'    : '#e94560',
    'Stage_A'       : '#f5a623',
    'Stage_B'       : '#f5a623',
    'Stage_C'       : '#f5a623',
    'Sound_Hub'     : '#50fa7b',
    'Tent_Storage'  : '#8be9fd',
    'Generator_Zone': '#bd93f9',
}

node_color_list = [node_colors_map.get(n, '#ffffff') for n in G.nodes()]

# Manual positions for a clear layout
pos = {
    'Main_Depot'    : (0, 0),
    'Tent_Storage'  : (-2, 1.5),
    'Sound_Hub'     : (2, 1.5),
    'Generator_Zone': (0, 2.5),
    'Stage_A'       : (-3, 3.5),
    'Stage_B'       : (1, 4.0),
    'Stage_C'       : (-1, 4.5),
}

# ---- Plot 1: Full Network ----
ax1 = axes[0]
ax1.set_facecolor('#16213e')
ax1.set_title('🎵 Festival Equipment Network\n(Edge weights = travel time in minutes)',
              color='white', fontsize=13, pad=15, fontweight='bold')

nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_color_list,
                       node_size=1200, alpha=0.95)
nx.draw_networkx_labels(G, pos, ax=ax1, font_size=7.5,
                        font_color='black', font_weight='bold')

edge_colors = ['#aaaaaa' if G[u][v]['road_type'] == 'paved' else '#665544'
               for u, v in G.edges()]
nx.draw_networkx_edges(G, pos, ax=ax1, edge_color=edge_colors,
                       width=2, alpha=0.7)

edge_labels = {(u, v): f"{d['weight']}m" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1,
                             font_size=7, font_color='white',
                             bbox=dict(boxstyle='round,pad=0.2',
                                       facecolor='#1a1a2e', alpha=0.7))

legend_elements = [
    mpatches.Patch(color='#e94560', label='Main Depot'),
    mpatches.Patch(color='#f5a623', label='Stage'),
    mpatches.Patch(color='#50fa7b', label='Sound Hub'),
    mpatches.Patch(color='#8be9fd', label='Tent Storage'),
    mpatches.Patch(color='#bd93f9', label='Generator Zone'),
]
ax1.legend(handles=legend_elements, loc='lower left',
           facecolor='#1a1a2e', labelcolor='white', fontsize=8)
ax1.axis('off')

# ---- Plot 2: Highlighted Shortest Paths ----
ax2 = axes[1]
ax2.set_facecolor('#16213e')
ax2.set_title('🗺️  Shortest Paths from Main Depot to Stages\n(Dijkstra\'s Algorithm)',
              color='white', fontsize=13, pad=15, fontweight='bold')

nx.draw_networkx_nodes(G, pos, ax=ax2, node_color=node_color_list,
                       node_size=1200, alpha=0.95)
nx.draw_networkx_labels(G, pos, ax=ax2, font_size=7.5,
                        font_color='black', font_weight='bold')
nx.draw_networkx_edges(G, pos, ax=ax2, edge_color='#333355',
                       width=1.5, alpha=0.4)

path_colors = {'Stage_A': '#ff6b6b', 'Stage_B': '#ffd93d', 'Stage_C': '#6bcb77'}

for target, info in results.items():
    path_edges = list(zip(info['path'], info['path'][1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, ax=ax2,
                           edge_color=path_colors[target], width=4, alpha=0.9)

legend2 = [
    mpatches.Patch(color='#ff6b6b', label=f"→ Stage_A  ({results['Stage_A']['time']} min)"),
    mpatches.Patch(color='#ffd93d', label=f"→ Stage_B  ({results['Stage_B']['time']} min)"),
    mpatches.Patch(color='#6bcb77', label=f"→ Stage_C  ({results['Stage_C']['time']} min)"),
]
ax2.legend(handles=legend2, loc='lower left',
           facecolor='#1a1a2e', labelcolor='white', fontsize=9)
ax2.axis('off')

plt.tight_layout(pad=3)
output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(output_dir, exist_ok=True)
viz_path = os.path.join(output_dir, 'network_visualization.png')
plt.savefig(viz_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e')
print(f"\n✅ Network visualization saved → {viz_path}")

# ── 6. Save Solution Output ───────────────────────────────────
output_txt = os.path.join(output_dir, 'solution_output.txt')
with open(output_txt, 'w', encoding='utf-8') as f:
    f.write("MUSIC FESTIVAL EQUIPMENT LOGISTICS - SOLUTION OUTPUT\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges\n\n")
    f.write("SHORTEST PATHS FROM MAIN DEPOT\n")
    f.write("-" * 40 + "\n")
    for target, info in results.items():
        f.write(f"\nTarget  : {target}\n")
        f.write(f"Route   : {' -> '.join(info['path'])}\n")
        f.write(f"Time    : {info['time']} minutes\n")
    f.write("\n\nALL-PAIRS SHORTEST PATH MATRIX\n")
    f.write("-" * 40 + "\n")
    f.write(matrix_df.to_string())

print(f"✅ Solution output saved    → {output_txt}")
print("\n🎉 Analysis complete!")
