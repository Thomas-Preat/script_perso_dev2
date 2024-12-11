Simplement telecharger le fichier zip directement du repo.

Ouvrir le terminal dans le dossier racine.

Utiliser les commandes :

*AJOUT DE FICHIER CSV*<br />
python main.py --import_files <file_name.csv><br />


*VOIR L'INVENTAIRE*<br />
python main.py --view<br />


*RECHERCHER DES ARTICLES*<br />
python main.py --search <"column:criteria"><br />
python main.py --search <"column:criteria"> <"column:criteria"><br />

ex:<br />
python main.py --search "name:Apple"<br />
python main.py --search "name:Apple" "category:Fruit"<br />


*GENERATION DE RAPPORT* <br />
python main.py --report


*SUPPRIMER UN ARTICLE*<br />
python main.py --delete <ID><br />


*AJOUTER UN ARTICLE*<br />
python main.py --add_product <"Name" Quantity Price "Category"><br />

ex:<br />
python main.py --add_product "Apple" 10 1.2 "Fruit"<br />
