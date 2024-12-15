import csv


def import_csv_files(file_paths, db_conn):
    cursor = db_conn.cursor()
    for file_path in file_paths:
        with open(file_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO inventory (name, quantity, price, category)
                    VALUES (?, ?, ?, ?)
                """, (
                    row["name"],
                    int(row["quantity"]),
                    float(row["price"]),
                    row["category"])
                    )
    db_conn.commit()
    print("Fichiers importés avec succès.")
