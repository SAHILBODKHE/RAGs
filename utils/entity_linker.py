def extract_entity_tables(user_input: str, table_list: list[str]) -> list[str]:
    user_input_lower = user_input.lower()
    matched = [table for table in table_list if table.lower().replace('_', ' ') in user_input_lower]
    return matched or ["claims"]  # fallback if nothing matched
