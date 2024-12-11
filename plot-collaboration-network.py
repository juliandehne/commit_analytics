import networkx as nx
import matplotlib.pyplot as plt
import polars as pl
import json

with open("contributors.json") as f:
    data = json.load(f)

with open("gesis_users.txt") as f:
    gesis_users = [l.strip() for l in f.readlines()]

twomode = []
for repo, contributors in data.items():
    for contributor in contributors:
        twomode.append(
            {
                "repository": repo,
                "account": contributor["login"],
                "contributions": contributor["contributions"],
            }
        )

df = pl.DataFrame(twomode).with_row_index()

df_nodes = (
    df.group_by("account")
    .agg(pl.col("contributions").sum())
    .with_columns(pl.col("account").is_in(gesis_users).alias("gesis"))
)

coocurrence = (
    df.join(df, on="repository")
    .filter(pl.col("index") < pl.col("index_right"))
    .group_by(["account", "account_right"])
    .len("weight")
    .sort(["weight", "account", "account_right"])
)

# Create graph
G = nx.Graph()
for row in df_nodes.iter_rows():
    G.add_node(row[0], contributions=row[1], gesis=row[2])

for row in coocurrence.iter_rows():
    G.add_edge(row[0], row[1], weight=row[2])

# Remove nodes with n hops or more to the center node
center_node = "schochastics"
nodes_to_remove = [
    node for node in G.nodes() if nx.shortest_path_length(G, center_node, node) >= 2
]
G.remove_nodes_from(nodes_to_remove)

# Calculate node degrees for scaling node sizes

node_sizes = {}
node_labels = {}
for node in G.nodes():
    if G.nodes()[node]["contributions"] >= 49 or G.nodes[node]["gesis"]:
        # node_sizes.append(G.degree(node) * 100)
        node_sizes[node] = G.degree(node) * 25
        node_labels[node] = node
    else:
        # node_sizes.append(1)
        node_sizes[node] = 1
        node_labels[node] = ""

edge_colors = [(0.0, 0.23, 0.47, e[2]["weight"] / 10) for e in G.edges(data=True)]

# GESIS colors (from website)
colors = {
    "purple": (0.39, 0.16, 0.47),
    "darkblue": (0, 0.23, 0.47),
    "blue": (0.05, 0.43, 0.99),
    "lightblue": (0.3, 0.61, 0.79),
}

# Visualize the network
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(G, k=5, seed=42, iterations=500)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=[colors["lightblue"]],
    node_size=[v for v in node_sizes.values()],
    labels=node_labels,
    font_size=12,
    font_color="black",
    edge_color=edge_colors,
    width=[G[u][v]["weight"] for u, v in G.edges()],
)

plt.title("Collaborator Network")
# plt.show()
plt.savefig("collaborator_network.pdf", facecolor="white", transparent=True)