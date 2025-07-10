import sqlparse
import re

def parse_schema(schema_path):
    with open(schema_path, "r") as f:
        content = f.read()
    statements = sqlparse.split(content)
    tables = []
    for stmt in statements:
        if "CREATE TABLE" in stmt:
            table_match = re.search(r"CREATE TABLE (\w+)", stmt, re.IGNORECASE)
            if table_match:
                table_name = table_match.group(1)
                columns = re.findall(r"(\w+)\s+\w+", stmt)
                tables.append({"table_name": table_name, "columns": columns})
    return tables
