import unittest
import sqlite3

from task_4_advanced_data_processing import (
    calculate_average_bmi,
    find_pokemon_with_highest_bmi,
    analyze_height_weight_ratio,
    classify_weight_category,
    assign_weight_categories,
)


class TestPokemonDataAnalysis(unittest.TestCase):
    """
    A test suite for analyzing Pokemon data stored in an SQLite database.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up a temporary in-memory SQLite database connection for testing.
        """
        cls.connection = sqlite3.connect(':memory:')
        cursor = cls.connection.cursor()
        cursor.execute('''
            CREATE TABLE pokemon_data (
                id INTEGER PRIMARY KEY,
                name TEXT,
                height REAL,
                weight REAL,
                bmi REAL
            )
        ''')
        cls.connection.commit()
        cursor.close()
    
    def test_calculate_average_bmi(self):
        """
        Test the calculate_average_bmi function.
        """
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('pokemon', 0.7, 6.9, 14.08)")
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('poky', 1.0, 13.0, 13.0)")
        self.connection.commit()
        
        average_bmi = calculate_average_bmi(self.connection)
        self.assertAlmostEqual(average_bmi, 13.54, places=2)
    
    def test_find_pokemon_with_highest_bmi(self):
        """
        Test the find_pokemon_with_highest_bmi function.
        """
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('pokemon', 0.7, 6.9, 14.08)")
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('poky', 1.0, 13.0, 13.0)")
        self.connection.commit()
        
        pokemon_with_highest_bmi = find_pokemon_with_highest_bmi(self.connection)
        self.assertEqual(pokemon_with_highest_bmi, 'pokemon')
    
    def test_analyze_height_weight_ratio(self):
        """
        Test the analyze_height_weight_ratio function.
        """
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('pokemon', 0.7, 6.9, 14.08)")
        cursor.execute("INSERT INTO pokemon_data (name, height, weight, bmi) VALUES ('poky', 1.0, 13.0, 13.0)")

        self.connection.commit()
        import sys
        from io import StringIO
        saved_stdout = sys.stdout
        sys.stdout = StringIO()
        
        analyze_height_weight_ratio(self.connection)
        output = sys.stdout.getvalue()
        expected_output = 'Average Height: 0.85\nAverage Weight: 9.95\nCorrelation Coefficient (Height-Weight): 1.00\n'
        print('output             ', output)
        print('expected_output', expected_output)
        self.assertEqual(output, expected_output)
        
        sys.stdout = saved_stdout
    
    def test_classify_weight_category(self):
        """
        Test the classify_weight_category function.
        """
        self.assertEqual(classify_weight_category(40), 'Light')
        self.assertEqual(classify_weight_category(70), 'Medium')
        self.assertEqual(classify_weight_category(110), 'Heavy')
    

if __name__ == '__main__':
    unittest.main()
