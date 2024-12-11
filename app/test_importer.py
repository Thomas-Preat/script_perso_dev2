import sqlite3
import os
from importer import import_csv_files

def test_import_csv_files():
    db_path = "test_inventory.db"
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE inventory (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL,
            category TEXT
        )
    """)
    import_csv_files(["test_data.csv"], conn)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM inventory")
    count = cursor.fetchone()[0]
    assert count > 0  # Vérifie que des données ont été insérées
    conn.close()
    os.remove(db_path)
