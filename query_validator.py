def validate_sql(sql: str, user_id: str, allowed_tables: list) -> bool:
    if any(keyword in sql.upper() for keyword in ["UPDATE", "DELETE", "DROP", "CREATE"]):
        return False
    if f"user_id = '{user_id}'" not in sql:
        return False
    return True
