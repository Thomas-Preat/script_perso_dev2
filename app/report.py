import csv


def generate_summary_report(db_conn, output_file):
    cursor = db_conn.cursor()
    cursor.execute("""
        SELECT category, COUNT(*), SUM(quantity), SUM(price * quantity)
        FROM inventory
        GROUP BY category
    """)
    rows = cursor.fetchall()

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Category",
             "Number of Products",
             "Total Quantity",
             "Total Value"]
            )
        writer.writerows(rows)
