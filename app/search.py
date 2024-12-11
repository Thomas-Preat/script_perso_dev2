def search_products(db_conn, search_criteria):
    cursor = db_conn.cursor()
    query = "SELECT * FROM inventory"
    values = []

    if search_criteria:  # Si des critères de recherche sont fournis
        query += " WHERE "
        conditions = []
        for criteria in search_criteria:
            if ":" in criteria:
                key, value = criteria.split(":")
                conditions.append(f"{key} LIKE ?")
                values.append(f"%{value}%")
        query += " AND ".join(conditions)

    cursor.execute(query, values)
    results = cursor.fetchall()

    for result in results:
        print(result)
