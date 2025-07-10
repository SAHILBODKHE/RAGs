import re

def parse_schema_sql(path):
    with open(path, 'r') as f:
        sql = f.read()

    table_pattern = r'CREATE TABLE `?(\w+)`?\s*\((.*?)\);'
    fk_pattern = r'FOREIGN KEY\s*\(`?(\w+)`?\)\s+REFERENCES\s+`?(\w+)`?\s*\(`?(\w+)`?\)'

    schema = {}

    for table_match in re.finditer(table_pattern, sql, re.DOTALL | re.IGNORECASE):
        table_name, columns_block = table_match.groups()
        column_lines = columns_block.splitlines()

        columns = []
        foreign_keys = {}

        for line in column_lines:
            line = line.strip().strip(',')
            if line.upper().startswith('FOREIGN KEY'):
                fk_match = re.search(fk_pattern, line, re.IGNORECASE)
                if fk_match:
                    col, ref_table, ref_col = fk_match.groups()
                    foreign_keys[col] = f"{ref_table}.{ref_col}"
            elif line and not line.upper().startswith(('PRIMARY', 'UNIQUE', 'KEY', 'CONSTRAINT', 'CHECK')):
                col_name = line.split()[0].strip('`')
                columns.append(col_name)

        schema[table_name] = {
            'columns': columns,
            'foreign_keys': foreign_keys
        }

    print(f"✅ Parsed {len(schema)} tables: {list(schema.keys())}")
    return schema
