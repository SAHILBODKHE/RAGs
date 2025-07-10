
def validate_sql(sql, user_id, allowed_tables):
    lowered = sql.lower()
    if "delete" in lowered or "update" in lowered or "drop" in lowered:
        return False, "Dangerous SQL command detected."
    if f"user_id = '{user_id}'" not in lowered:
        return False, "Missing user_id filter."
    for word in lowered.split():
        if word in ["from", "join"]:
            for table in allowed_tables:
                if table in lowered:
                    break
            else:
                return False, "Table not in graph scope."
    return True, ""
