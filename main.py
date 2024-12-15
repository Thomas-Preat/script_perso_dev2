from app.importer import import_csv_files
from app.database import (
    initialize_database,
    display_all_data,
    delete_item_by_id,
    add_product
)
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
        try:
            choice = input("\nEntrez le numéro de votre choix : ").strip()
            #
            # Premiere option
            #
            if choice == "1":
                try:
                    file_paths = input(
                        "Entrez les chemins des fichiers CSV à importer"
                        "(séparés par des espaces) : "
                        ).strip().split()
                    if not file_paths:
                        raise ValueError("Aucun chemin fourni.")
                    import_csv_files(file_paths, db_conn)
                except Exception as e:
                    print(f"Erreur lors de l'importation des fichiers : {e}")
            #
            # Deuxieme option
            #
            elif choice == "2":
                try:
                    search_criteria = input(
                        "Entrez vos critères de recherche"
                        "(ex. name:Apple category:Fruit) : "
                        ).strip().split()
                    if not search_criteria:
                        raise ValueError("Aucun critère de recherche fourni.")
                    search_products(db_conn, search_criteria)
                except Exception as e:
                    print(f"Erreur lors de la recherche : {e}")
            #
            # Troisieme option
            #
            elif choice == "3":
                try:
                    generate_summary_report(db_conn, "summary_report.csv")
                    print("Rapport récapitulatif généré : summary_report.csv")
                except Exception as e:
                    print(f"Erreur lors de la génération du rapport : {e}")
            #
            # Quatrieme option
            #
            elif choice == "4":
                try:
                    display_all_data(db_conn)
                except Exception as e:
                    print(f"Erreur lors de l'affichage des données : {e}")
            #
            # Cinquieme option
            #
            elif choice == "5":
                try:
                    item_id = input(
                        "Entrez l'ID de l'article à supprimer : "
                        ).strip()
                    if not item_id.isdigit():
                        raise ValueError("L'ID doit être un entier.")
                    rows_deleted = delete_item_by_id(db_conn, int(item_id))
                    if rows_deleted > 0:
                        print(f"L'article avec l'ID {item_id} a été supprimé.")
                    else:
                        print(f"Aucun article trouvé avec l'ID {item_id}.")
                except Exception as e:
                    print(f"Erreur lors de la suppression de l'article : {e}")
            #
            # Sixieme option
            #
            elif choice == "6":
                try:
                    name = input("Entrez le nom du produit : ").strip()
                    if not name:
                        raise ValueError(
                            "Le nom du produit ne peut pas être vide."
                            )
                    quantity = input("Entrez la quantité : ").strip()
                    if not quantity.isdigit():
                        raise ValueError("La quantité doit être un entier.")
                    quantity = int(quantity)

                    price = input("Entrez le prix : ").strip()
                    try:
                        price = float(price)
                    except ValueError:
                        raise ValueError(
                            "Le prix doit être un nombre décimal."
                            )
                    category = input("Entrez la catégorie : ").strip()
                    if not category:
                        raise ValueError("La catégorie ne peut pas être vide.")
                    add_product(db_conn, name, quantity, price, category)
                    print(
                        f"Produit ajouté : {name}, quantité : {quantity},"
                        " prix : {price}, catégorie : {category}"
                        )
                except Exception as e:
                    print(f"Erreur lors de l'ajout du produit : {e}")
            #
            # Septieme option
            #
            elif choice == "7":
                print(
                    "Merci d'avoir utilisé le système de gestion d'inventaire."
                    "Au revoir !"
                    )
                break
            else:
                print(
                    "Choix invalide. Veuillez entrer un numéro entre 1 et 7."
                    )
        except Exception as e:
            print(f"Une erreur inattendue est survenue : {e}")
    db_conn.close()


if __name__ == "__main__":
    main()
