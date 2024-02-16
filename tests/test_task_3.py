import sqlite3
import unittest
from task_3_fill_db import create_pokemon_table_if_not_exists, load_pokemon_data_into_db

class TestPokemonDBFunctions(unittest.TestCase):
    """
    A test suite for database functions related to Pokemon data.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up a temporary in-memory SQLite database connection for testing.
        """
        cls.connection = sqlite3.connect(':memory:')
    
    def setUp(self):
        """
        Set up the test environment by dropping the 'pokemon_data' table if it exists.
        """
        self.connection.executescript("""
            DROP TABLE IF EXISTS pokemon_data;
        """)
    
    def test_create_pokemon_table_if_not_exists(self):
        """
        Test the create_pokemon_table_if_not_exists function.
        """
        create_pokemon_table_if_not_exists(self.connection)
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon_data';")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
    
    def test_load_pokemon_data_into_db(self):
        """
        Test the load_pokemon_data_into_db function.
        """
        data = {
            '1': {'name': 'Bulbasaur', 'height': 0.7, 'weight': 6.9, 'bmi': 14.08},
            '2': {'name': 'Ivysaur', 'height': 1.0, 'weight': 13.0, 'bmi': 13.0},
        }
        create_pokemon_table_if_not_exists(self.connection)
        load_pokemon_data_into_db(self.connection, data)
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM pokemon_data;")
        result = cursor.fetchall()
        self.assertEqual(len(result), len(data))

if __name__ == '__main__':
    unittest.main()
