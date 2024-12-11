import sqlite3

def initialize_database(db_path="inventory.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT,
            quantity INTEGER,
            price REAL,
            category TEXT
        )
    """)
    conn.commit()
    return conn

def display_all_data(db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def delete_item_by_id(db_conn, item_id):
    cursor = db_conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    db_conn.commit()
    return cursor.rowcount  # Retourne le nombre de lignes affectées

def add_product(db_conn, name, quantity, price, category):
    """Ajoute un produit dans la table inventory"""
    cursor = db_conn.cursor()
    cursor.execute('''
        INSERT INTO inventory (name, quantity, price, category)
        VALUES (?, ?, ?, ?)
    ''', (name, quantity, price, category))
    db_conn.commit()
