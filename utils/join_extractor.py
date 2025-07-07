import re

def extract_join_hints_from_schema(schema: str) -> list[str]:
    joins = []
    tables = schema.split("CREATE TABLE")
    for table in tables:
        lines = table.strip().splitlines()
        if not lines:
            continue
        table_name = lines[0].split()[0]
        for line in lines:
            match = re.search(r'FOREIGN KEY\s*\((\w+)\)\s+REFERENCES\s+(\w+)\((\w+)\)', line)
            if match:
                fk_col, ref_table, ref_col = match.groups()
                joins.append(f"JOIN {ref_table} ON {table_name}.{fk_col} = {ref_table}.{ref_col}")
    return joins
