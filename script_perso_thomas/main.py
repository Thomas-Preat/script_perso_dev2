import argparse
from app.importer import import_csv_files
from app.database import initialize_database, display_all_data
from app.search import search_products
from app.report import generate_summary_report

def main():
    parser = argparse.ArgumentParser(description="Système de gestion d'inventaire")
    parser.add_argument("--import_files", nargs="+", help="Importer des fichiers CSV (liste des chemins)")
    parser.add_argument("--search", nargs="+", help="Rechercher des produits (nom, catégorie, etc.)")
    parser.add_argument("--report", help="Générer un rapport récapitulatif", action="store_true")
    parser.add_argument("--view", help="Afficher toutes les données", action="store_true")
    parser.add_argument("--delete", type=int, help="Supprime un article par son ID.")

    args = parser.parse_args()

    db_conn = initialize_database()

    if args.import_files:
        import_csv_files(args.import_files, db_conn)
    elif args.search:
        search_products(db_conn, args.search)
    elif args.report:
        generate_summary_report(db_conn)
    elif args.view:
        display_all_data(db_conn)
    elif args.delete:
        from app.database import delete_item_by_id
        rows_deleted = delete_item_by_id(db_conn, args.delete)
        if rows_deleted > 0:
            print(f"L'article avec l'ID {args.delete} a été supprimé.")
        else:
            print(f"Aucun article trouvé avec l'ID {args.delete}.")
    else:
        parser.print_help()

    db_conn.close()

if __name__ == "__main__":
    main()

