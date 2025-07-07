def get_related_tables(graph: dict, start_tables: list[str], depth: int = 2) -> set:
    """
    Traverse the schema graph to find all related tables up to a given depth.
    Useful for pruning only the relevant schema subset for prompting.
    """
    visited = set()
    frontier = set(start_tables)

    for _ in range(depth):
        next_frontier = set()
        for table in frontier:
            if table in graph:
                next_frontier.update(graph[table])
        visited.update(frontier)
        frontier = next_frontier - visited

    return visited.union(frontier)
