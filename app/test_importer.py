import unittest
from unittest.mock import patch
import os
import io
import sqlite3
import csv

from importer import import_csv_files
from database import (
    initialize_database, display_all_data,
    delete_item_by_id, add_product
)
from search import search_products
from report import generate_summary_report


class TestImporter(unittest.TestCase):

    def setUp(self):
        """Créer une base de données temporaire pour les tests"""
        self.db_filename = ":memory:"
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()
        self.create_inventory_table()

    def tearDown(self):
        """Fermer la connexion après chaque test et supprimer le fichier CSV"""
        self.conn.close()
        if os.path.exists("summary_report.csv"):
            os.remove("summary_report.csv")

    def create_inventory_table(self):
        """Créer la table d'inventaire pour les tests"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def test_initialize_database(self):
        """Test de l'initialisation de la base de données"""
        # Remplacer la connexion en mémoire par un chemin de fichier
        # pour l'initialisation de la DB
        db_path = ":memory:"  # ou un chemin de fichier valide
        initialize_database(db_path)

        # Vérifier que la table 'inventory' existe
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master" +
            " WHERE type='table' AND name='inventory'"
            )
        result = cursor.fetchone()

        # Le test passera si la table 'inventory' existe
        self.assertIsNotNone(result, "La table 'inventory' n'a pas été créée.")

    def test_import_csv_files(self):
        """Test d'importation des fichiers CSV"""
        test_data = (
            "name,quantity,price,category\n"
            "Apple,10,1.2,Fruit\nBanana,20,0.8,Fruit"
            )
        with open("test.csv", "w") as f:
            f.write(test_data)

        # Passer la connexion à la base de données
        # à la fonction import_csv_files
        import_csv_files(["test.csv"], self.conn)

        # Vérifier l'insertion des données
        self.cursor.execute("SELECT * FROM inventory WHERE name='Apple'")
        result = self.cursor.fetchone()
        print("DEBUG: Result after insertion:", result)  # Debugging line
        # Vérifier si le produit "Apple" est trouvé
        self.assertIsNotNone(result)
        # Vérifier que le nom correspond à "Apple"
        self.assertEqual(result[1], 'Apple')

        os.remove("test.csv")

    def test_add_product(self):
        """Test de l'ajout d'un produit"""
        # Ajouter un produit à la base de données
        add_product(self.conn, "Apple", 10, 1.2, "Fruit")

        # Vérifier que le produit a bien été ajouté
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE name='Apple'")
        result = cursor.fetchone()

        self.assertIsNotNone(result)  # Le produit doit être trouvé
        self.assertEqual(result[1], "Apple")  # Vérifier le nom du produit
        self.assertEqual(result[2], 10)  # Vérifier la quantité
        self.assertEqual(result[3], 1.2)  # Vérifier le prix
        self.assertEqual(result[4], "Fruit")  # Vérifier la catégorie

    def test_delete_item_by_id(self):
        """Test de la suppression d'un produit par son ID"""
        # Ajouter un produit à la base de données
        add_product(self.conn, "Banana", 20, 0.8, "Fruit")

        # Vérifier que le produit a bien été ajouté avant la suppression
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE name='Banana'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)  # Le produit doit être trouvé

        # Supprimer le produit par son ID
        item_id = result[0]  # Récupérer l'ID du produit
        deleted_count = delete_item_by_id(self.conn, item_id)

        # Vérifier que la suppression a bien eu lieu
        self.assertEqual(deleted_count, 1)  # Une ligne a été supprimée

        # Vérifier que le produit n'est plus dans la base de données
        cursor.execute("SELECT * FROM inventory WHERE name='Banana'")
        result_after_delete = cursor.fetchone()
        # Le produit ne doit plus exister
        self.assertIsNone(result_after_delete)

    def test_display_all_data(self):
        """Test de l'affichage de toutes les données"""
        # Ajouter des produits à la base de données
        add_product(self.conn, "Apple", 10, 1.2, "Fruit")
        add_product(self.conn, "Banana", 20, 0.8, "Fruit")

        # Rediriger la sortie de `display_all_data` pour capturer l'affichage
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            # Appeler la fonction pour afficher les données
            display_all_data(self.conn)

            # Vérifier que les produits sont affichés correctement
            output = captured_output.getvalue()
            # Vérifier que "Apple" est dans l'affichage
            self.assertIn("Apple", output)
            # Vérifier que "Banana" est dans l'affichage
            self.assertIn("Banana", output)


class TestReport(unittest.TestCase):

    def setUp(self):
        """Créer une base de données temporaire pour les tests"""
        self.db_filename = ":memory:"
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()
        self.create_inventory_table()

    def tearDown(self):
        """Fermer la connexion après chaque test et supprimer le fichier CSV"""
        self.conn.close()
        if os.path.exists("test_file.csv"):
            os.remove("test_file.csv")

    def create_inventory_table(self):
        """Créer la table d'inventaire pour les tests"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def test_generate_summary_report_with_data(self):
        """Test de la génération du rapport avec des données dans la base"""
        # Ajouter des données fictives à la table
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction qui génère le rapport
        generate_summary_report(self.conn, "test_file.csv")

        # Vérifier que le fichier "test_file.csv"
        # existe bien après la génération
        self.assertTrue(os.path.exists("test_file.csv"))

        # Vérifier le contenu du fichier CSV
        with open("test_file.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

            # Vérifier les en-têtes
            self.assertEqual(
                rows[0], ["Category", "Number of Products",
                          "Total Quantity", "Total Value"]
                )

            # Vérifier les données du rapport
            self.assertEqual(rows[1], ['Fruit', '2', '30', '28.0'])
            self.assertEqual(rows[2], ['Vegetable', '2', '45', '30.0'])

    def test_generate_summary_report_with_no_data(self):
        """Test de la génération du rapport
        lorsque la base de données est vide"""
        # Appeler la fonction qui génère le rapport
        # (aucune donnée dans la table)
        generate_summary_report(self.conn, "test_file.csv")

        # Vérifier que le fichier "test_file.csv"
        # existe bien après la génération
        self.assertTrue(os.path.exists("test_file.csv"))

        # Vérifier le contenu du fichier CSV
        with open("test_file.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

            # Vérifier que seule la ligne d'en-têtes est présente
            self.assertEqual(
                rows, [["Category", "Number of Products",
                        "Total Quantity", "Total Value"]]
                )

    def test_generate_summary_report_empty_categories(self):
        """Test génération du rapport si certaines catégories sont vides"""
        # Ajouter des produits dans une seule catégorie
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction qui génère le rapport
        generate_summary_report(self.conn, "test_file.csv")

        # Vérifier que le fichier "test_file.csv"
        # existe bien après la génération
        self.assertTrue(os.path.exists("test_file.csv"))

        # Vérifier le contenu du fichier CSV
        with open("test_file.csv", "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

            # Vérifier les en-têtes
            self.assertEqual(
                rows[0], ["Category", "Number of Products",
                          "Total Quantity", "Total Value"]
                )

            # Vérifier les données du rapport
            self.assertEqual(rows[1], ['Fruit', '2', '30', '28.0'])
            self.assertEqual(rows[2], ['Vegetable', '1', '30', '15.0'])


class TestSearchProducts(unittest.TestCase):

    def setUp(self):
        """Créer une base de données temporaire pour les tests"""
        self.db_filename = ":memory:"
        self.conn = sqlite3.connect(self.db_filename)
        self.cursor = self.conn.cursor()
        self.create_inventory_table()

    def tearDown(self):
        """Fermer la connexion après chaque test"""
        self.conn.close()

    def create_inventory_table(self):
        """Créer la table d'inventaire pour les tests"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def test_search_products_with_single_criteria(self):
        """Test de recherche avec un seul critère"""
        # Ajouter des produits à la base de données
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction avec un critère de recherche
        # (par exemple, "name:Apple")
        search_criteria = ["name:Apple"]
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            search_products(self.conn, search_criteria)

            # Vérifier que le produit "Apple" est trouvé
            output = captured_output.getvalue().strip()
            self.assertIn("Apple", output)
            self.assertNotIn("Banana", output)
            self.assertNotIn("Carrot", output)
            self.assertNotIn("Broccoli", output)

    def test_search_products_with_multiple_criteria(self):
        """Test de recherche avec plusieurs critères"""
        # Ajouter des produits à la base de données
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Vérification que les produits sont insérés
        self.cursor.execute("SELECT * FROM inventory")
        all_products = self.cursor.fetchall()
        self.assertEqual(
            len(all_products), 4,
            "Les produits n'ont pas été correctement insérés."
            )

        # Appeler la fonction avec plusieurs critères de recherche
        # (par exemple, "name:Apple" et "category:Fruit")
        search_criteria = ["name:Apple", "category:Fruit"]
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            search_products(self.conn, search_criteria)

            # Vérifier que le produit "Apple" et "Banana" sont trouvés
            output = captured_output.getvalue().strip()
            self.assertIn("Apple", output)  # "Apple" devrait être trouvé
            self.assertNotIn("Banana", output)
            self.assertNotIn("Carrot", output)
            self.assertNotIn("Broccoli", output)

    def test_search_products_with_no_results(self):
        """Test de recherche de critères ne correspondant à aucun produit"""
        # Ajouter des produits à la base de données
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction avec des critères
        # qui ne correspondent à aucun produit
        search_criteria = ["name:Orange"]
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            search_products(self.conn, search_criteria)

            # Vérifier qu'aucun résultat n'est trouvé
            output = captured_output.getvalue().strip()
            # Aucun résultat trouvé, donc sortie vide
            self.assertEqual(output, "")

    def test_search_products_with_wildcards(self):
        """Test de recherche avec des critères incluant des jokers"""
        # Ajouter des produits à la base de données
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction avec un critère incluant un joker
        # par exemple "name:Ap"
        search_criteria = ["name:Ap"]
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            search_products(self.conn, search_criteria)

            # Vérifier que le produit "Apple" est trouvé
            output = captured_output.getvalue().strip()
            self.assertIn("Apple", output)
            self.assertNotIn("Banana", output)
            self.assertNotIn("Carrot", output)
            self.assertNotIn("Broccoli", output)

    def test_search_products_empty_criteria(self):
        """Test de recherche avec une liste de critères vide"""
        # Ajouter des produits à la base de données
        self.cursor.executemany('''
            INSERT INTO inventory (name, quantity, price, category)
            VALUES (?, ?, ?, ?)
        ''', [
            ('Apple', 10, 1.2, 'Fruit'),
            ('Banana', 20, 0.8, 'Fruit'),
            ('Carrot', 30, 0.5, 'Vegetable'),
            ('Broccoli', 15, 1.0, 'Vegetable')
        ])
        self.conn.commit()

        # Appeler la fonction avec une liste vide de critères de recherche
        search_criteria = []
        with patch('sys.stdout', new_callable=io.StringIO) as captured_output:
            search_products(self.conn, search_criteria)

            # Vérifier que tous les produits sont trouvés
            # (aucun critère de recherche)
            output = captured_output.getvalue().strip()
            self.assertIn("Apple", output)
            self.assertIn("Banana", output)
            self.assertIn("Carrot", output)
            self.assertIn("Broccoli", output)


if __name__ == "__main__":
    unittest.main()
