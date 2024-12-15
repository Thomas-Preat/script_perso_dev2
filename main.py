import argparse
from app.importer import import_csv_files
from app.database import initialize_database, display_all_data, delete_item_by_id, add_product
from app.search import search_products
from app.report import generate_summary_report

def main():
    print("Bienvenue dans le système de gestion d'inventaire")
    db_conn = initialize_database()

    while True:
        print("\nQue voulez-vous faire ?")
        print("1 : Importer un ou plusieurs fichiers CSV")
        print("2 : Rechercher des produits")
        print("3 : Générer un rapport récapitulatif")
        print("4 : Afficher toutes les données")
        print("5 : Supprimer un article par ID")
        print("6 : Ajouter un produit")
        print("7 : Quitter le programme")
        choice = input("\nEntrez le numéro de votre choix : ")

        if choice == "1":
            file_paths = input("Entrez les chemins des fichiers CSV à importer (séparés par des espaces) : ").split()
            if file_paths:
                import_csv_files(file_paths, db_conn)
        elif choice == "2":
            search_criteria = input("Entrez vos critères de recherche (ex. name:Apple category:Fruit) : ").split()
            if search_criteria:
                search_products(db_conn, search_criteria)
        elif choice == "3":
            generate_summary_report(db_conn, "summary_report.csv")
            print("Rapport récapitulatif généré : summary_report.csv")
        elif choice == "4":
            display_all_data(db_conn)
        elif choice == "5":
            try:
                item_id = int(input("Entrez l'ID de l'article à supprimer : "))
                rows_deleted = delete_item_by_id(db_conn, item_id)
                if rows_deleted > 0:
                    print(f"L'article avec l'ID {item_id} a été supprimé.")
                else:
                    print(f"Aucun article trouvé avec l'ID {item_id}.")
            except ValueError:
                print("Erreur : L'ID doit être un entier.")
        elif choice == "6":
            name = input("Entrez le nom du produit : ")
            try:
                quantity = int(input("Entrez la quantité : "))
                price = float(input("Entrez le prix : "))
                category = input("Entrez la catégorie : ")
                add_product(db_conn, name, quantity, price, category)
                print(f"Produit ajouté : {name}, quantité : {quantity}, prix : {price}, catégorie : {category}")
            except ValueError:
                print("Erreur : La quantité doit être un entier et le prix un nombre décimal.")
        elif choice == "7":
            print("Merci d'avoir utilisé le système de gestion d'inventaire. Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez entrer un numéro entre 1 et 7.")

    db_conn.close()

if __name__ == "__main__":
    main()


