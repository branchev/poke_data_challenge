import unittest
from unittest.mock import patch, mock_open
import apache_beam as beam
from task_2_data_transformation import (
    normalize_pokemon,
    calculate_bmi,
    update_json_file,
    run_pipeline,
)


class TestPokemonFunctions(unittest.TestCase):

    def setUp(self):
        self.pokemon_data = {
            'id': 1,
            'name': 'pokemon',
            'height': 70,  # 7 decimeters
            'weight': 699  # 69 hectograms
        }
        self.normalized_pokemon = {
            'id': 1,
            'name': 'pokemon',
            'height': 7.0,  # 0.7 meters
            'weight': 69.9  # 6.99 kilograms
        }

    def test_normalize_pokemon(self):
        normalized = normalize_pokemon(self.pokemon_data)
        self.assertEqual(normalized, self.normalized_pokemon)

    def test_calculate_bmi(self):
        bmi_calculated = calculate_bmi(self.normalized_pokemon)
        expected_bmi = round(69.9 / (7.0 ** 2), 2)
        self.assertEqual(bmi_calculated['bmi'], expected_bmi)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    @patch('json.dump')
    def test_update_json_file(self, mock_json_dump, mock_json_load, mock_open):
        mock_json_load.return_value = {}
        update_json_file(('1', self.normalized_pokemon))
        mock_open.assert_called_once_with('pokemon_details.json', 'r+')
        mock_json_dump.assert_called_once_with({'1': self.normalized_pokemon}, mock_open().__enter__(), indent=4)

    @patch('task_2_data_transformation.beam.Pipeline.run')
    @patch('task_2_data_transformation.beam.Pipeline.__enter__')
    @patch('task_2_data_transformation.beam.Pipeline.__exit__')
    def test_run_pipeline(self, mock_pipeline_exit, mock_pipeline_enter, mock_pipeline_run):
        mock_pipeline_run.return_value = None
        run_pipeline()
        mock_pipeline_enter.assert_called_once()
        self.assertTrue(mock_pipeline_exit.called)


if __name__ == '__main__':
    unittest.main()
