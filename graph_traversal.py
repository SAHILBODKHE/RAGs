import pickle
import networkx as nx

def get_related_tables(seed_tables, depth=2):
    with open("config/graph.pkl", "rb") as f:
        G = pickle.load(f)
    visited = set()
    for seed in seed_tables:
        visited.update(nx.single_source_shortest_path_length(G, seed, cutoff=depth).keys())
    return list(visited)
