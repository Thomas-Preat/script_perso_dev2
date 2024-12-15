import unittest
from unittest.mock import patch, MagicMock
import sqlite3
from app.database import initialize_database, add_product, display_all_data
from app.importer import import_csv_files
from app.search import search_products
from app.report import generate_summary_report
from main import main


class TestMain(unittest.TestCase):

    def setUp(self):
        """Préparer une base de données en mémoire pour les tests."""
        self.db_conn = sqlite3.connect(":memory:")
        self.cursor = self.db_conn.cursor()
        self.create_inventory_table()

    def tearDown(self):
        """Fermer la connexion à la base de données."""
        self.db_conn.close()

    def create_inventory_table(self):
        """Créer une table d'inventaire pour les tests."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.db_conn.commit()

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["1", "test.csv", "7"])
    @patch("app.importer.import_csv_files")
    def test_import_csv_files(self, mock_import_csv, mock_input, mock_initialize_db):
        """Tester l'importation de fichiers CSV via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_import_csv.assert_called_once_with(["test.csv"], mock_initialize_db.return_value)

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["2", "name:Apple", "7"])
    @patch("app.search.search_products")
    def test_search_products(self, mock_search_products, mock_input, mock_initialize_db):
        """Tester la recherche de produits via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_search_products.assert_called_once_with(mock_initialize_db.return_value, ["name:Apple"])

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["3", "7"])
    @patch("app.report.generate_summary_report")
    def test_generate_summary_report(self, mock_generate_report, mock_input, mock_initialize_db):
        """Tester la génération du rapport via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_generate_report.assert_called_once_with(mock_initialize_db.return_value, "summary_report.csv")

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["4", "7"])
    @patch("app.database.display_all_data")
    def test_display_all_data(self, mock_display_all_data, mock_input, mock_initialize_db):
        """Tester l'affichage de toutes les données via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_display_all_data.assert_called_once_with(mock_initialize_db.return_value)

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["5", "1", "7"])
    @patch("app.database.delete_item_by_id")
    def test_delete_item_by_id(self, mock_delete_item, mock_input, mock_initialize_db):
        """Tester la suppression d'un article via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_delete_item.assert_called_once_with(mock_initialize_db.return_value, 1)

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["6", "Apple", "10", "1.5", "Fruit", "7"])
    @patch("app.database.add_product")
    def test_add_product(self, mock_add_product, mock_input, mock_initialize_db):
        """Tester l'ajout d'un produit via le menu."""
        with patch("sys.stdout"):  # Ignorer les sorties
            main()

        mock_add_product.assert_called_once_with(mock_initialize_db.return_value, "Apple", 10, 1.5, "Fruit")

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["7"])
    def test_quit_program(self, mock_input, mock_initialize_db):
        """Tester la sortie propre du programme."""
        with patch("sys.stdout") as mock_stdout:
            main()

            output = mock_stdout.write.call_args_list
            output_text = ''.join(call[0][0] for call in output)
            self.assertIn("Merci d'avoir utilisé le système de gestion d'inventaire. Au revoir !", output_text)

    @patch("main.initialize_database", return_value=sqlite3.connect(":memory:"))
    @patch("builtins.input", side_effect=["invalid", "7"])
    def test_invalid_choice(self, mock_input, mock_initialize_db):
        """Tester un choix de menu invalide."""
        with patch("sys.stdout") as mock_stdout:
            main()

            output = mock_stdout.write.call_args_list
            output_text = ''.join(call[0][0] for call in output)
            self.assertIn("Choix invalide. Veuillez entrer un numéro entre 1 et 7.", output_text)


if __name__ == "__main__":
    unittest.main()
