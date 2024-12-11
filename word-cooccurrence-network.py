import re
import itertools
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import polars as pl

# Read lines from the file
lines = pl.read_parquet("commits.parquet").get_column("message").to_list()

# Preprocessing
# import nltk
# nltk.download('stopwords')
stop_words = set(stopwords.words("english"))
processed_lines = []


for line in lines:
    # Tokenize, clean, and normalize
    words = [
        word.lower()
        for word in word_tokenize(re.sub(r"\W+", " ", line.strip()))
        if word.lower() not in stop_words
        and not word.isdigit()  # Exclude stopwords and numeric tokens
    ]
    processed_lines.append(words)

# Define co-occurrence window size
window_size = 2

# Generate co-occurrences
co_occurrences = Counter()
for words in processed_lines:
    for i in range(len(words) - window_size + 1):
        window = words[i : i + window_size]
        co_occurrences.update(itertools.combinations(sorted(set(window)), 2))

# Create graph
G = nx.Graph()
for (word1, word2), weight in co_occurrences.items():
    G.add_edge(word1, word2, weight=weight)


nodes_to_remove = [node for node, degree in dict(G.degree()).items() if degree < 15]
G.remove_nodes_from(nodes_to_remove)

# Calculate node degrees for scaling node sizes
node_sizes = [G.degree(node) * 100 for node in G.nodes()]

# GESIS colors (from website)
colors = {
    "purple": (0.39, 0.16, 0.47),
    "darkblue": (0, 0.23, 0.47),
    "blue": (0.05, 0.43, 0.99),
    "lightblue": (0.3, 0.61, 0.79)
}

# Visualize the network
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=colors["lightblue"],
    node_size=node_sizes,
    font_size=12,
    font_color="black",
    edge_color=(0.0, 0.23, 0.47, 0.5),
)

plt.title("Word Co-occurrence Network")
# plt.show()
plt.savefig("commits_words_coocurrence.pdf", facecolor="white", transparent=True)
