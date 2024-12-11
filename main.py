import argparse
from app.importer import import_csv_files
from app.database import initialize_database, display_all_data, delete_item_by_id, add_product
from app.search import search_products
from app.report import generate_summary_report

def main():
    parser = argparse.ArgumentParser(description="Système de gestion d'inventaire")
    parser.add_argument("--import_files", nargs="+", help="Importer des fichiers CSV (liste des chemins)")
    parser.add_argument("--search", nargs="+", help="Rechercher des produits (nom, catégorie, etc.)")
    parser.add_argument("--report", help="Générer un rapport récapitulatif", action="store_true")
    parser.add_argument("--view", help="Afficher toutes les données", action="store_true")
    parser.add_argument("--delete", type=int, help="Supprime un article par son ID.")
    parser.add_argument("--add_product", nargs=4, metavar=("NAME", "QUANTITY", "PRICE", "CATEGORY"),
                        help="Ajouter un produit dans la base de données.")

    args = parser.parse_args()

    db_conn = initialize_database()

    if args.import_files:
        import_csv_files(args.import_files, db_conn)
    elif args.search:
        search_products(db_conn, args.search)
    elif args.report:
        generate_summary_report(db_conn, "summary_report.csv")
    elif args.view:
        display_all_data(db_conn)
    elif args.delete:
        from app.database import delete_item_by_id
        rows_deleted = delete_item_by_id(db_conn, args.delete)
        if rows_deleted > 0:
            print(f"L'article avec l'ID {args.delete} a été supprimé.")
        else:
            print(f"Aucun article trouvé avec l'ID {args.delete}.")
    elif args.add_product:
        name, quantity, price, category = args.add_product
        try:
            add_product(db_conn, name, int(quantity), float(price), category)
            print(f"Produit ajouté : {name}, quantité : {quantity}, prix : {price}, catégorie : {category}")
        except ValueError:
            print("Erreur : Assurez-vous que la quantité est un entier et que le prix est un nombre décimal.")
    else:
        parser.print_help()

    db_conn.close()

if __name__ == "__main__":
    main()

