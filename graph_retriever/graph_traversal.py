
def expand_graph(graph, seeds, depth):
    visited = set(seeds)
    frontier = list(seeds)
    for _ in range(depth):
        next_frontier = []
        for node in frontier:
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.append(neighbor)
        frontier = next_frontier
    return list(visited)
