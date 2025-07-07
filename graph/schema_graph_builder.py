import re
from collections import defaultdict

def build_schema_graph(schema: str) -> dict:
    """
    Parses the schema SQL and builds a directed graph of table relationships via foreign keys.
    Returns: dict[table_name] = list of referenced tables
    """
    graph = defaultdict(list)
    tables = schema.split('CREATE TABLE')

    for table_def in tables:
        lines = table_def.strip().splitlines()
        if not lines:
            continue
        table_name = lines[0].split()[0]
        for line in lines:
            fk_match = re.search(r'FOREIGN KEY\s*\((\w+)\)\s+REFERENCES\s+(\w+)\((\w+)\)', line)
            if fk_match:
                _, referenced_table, _ = fk_match.groups()
                graph[table_name].append(referenced_table)

    return dict(graph)
