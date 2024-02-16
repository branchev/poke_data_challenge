import sqlite3
import unittest
from task_3_fill_db import create_pokemon_table_if_not_exists, load_pokemon_data_into_db

class TestPokemonDBFunctions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
    
    def setUp(self):
        # Create a fresh in-memory database for each test case
        self.connection.executescript("""
            DROP TABLE IF EXISTS pokemon_data;
        """)
    
    def test_create_pokemon_table_if_not_exists(self):
        # Check if the table is created when it doesn't exist
        create_pokemon_table_if_not_exists(self.connection)
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pokemon_data';")
        result = cursor.fetchone()
        self.assertIsNotNone(result)  # Table should exist
    
    def test_load_pokemon_data_into_db(self):
        # Test loading data into the database
        data = {
            '1': {'name': 'Bulbasaur', 'height': 0.7, 'weight': 6.9, 'bmi': 14.08},
            '2': {'name': 'Ivysaur', 'height': 1.0, 'weight': 13.0, 'bmi': 13.0},
            # Add more sample data as needed
        }
        create_pokemon_table_if_not_exists(self.connection)
        load_pokemon_data_into_db(self.connection, data)
        
        # Verify that data is inserted correctly
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM pokemon_data;")
        result = cursor.fetchall()
        self.assertEqual(len(result), len(data))  # Check if all data is inserted

if __name__ == '__main__':
    unittest.main()
