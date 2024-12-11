Simplement telecharger le fichier zip directement du repo.

Ouvrir le terminal dans le dossier racine.

Utiliser les commandes :

AJOUT DE FICHIER CSV
python main.py --import_files <file_name.csv>


VOIR L'INVENTAIRE
python main.py --view


RECHERCHER DES ARTICLES
python main.py --search <"column:criteria">
python main.py --search <"column:criteria"> <"column:criteria">

ex:
python main.py --search "name:Apple"
python main.py --search "name:Apple" "category:Fruit"


GENERATION DE RAPPORT <br />
python main.py --report


SUPPRIMER UN ARTICLE
python main.py --delete <ID>


AJOUTER UN ARTICLE
python main.py --add_product <"Name Quantity Price Category">

ex:
python main.py --add_product "Apple 10 1.2 Fruit"
