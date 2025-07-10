
def build_join_graph(schema):
    graph = {table: [] for table in schema}
    for table, data in schema.items():
        for fk, ref in data["foreign_keys"].items():
            ref_table = ref.split(".")[0]
            graph[table].append(ref_table)
            graph[ref_table].append(table)
    return graph
