import json
import apache_beam as beam


class PrintFirstN(beam.DoFn):
    """A DoFn for printing the first N elements."""

    def __init__(self, n):
        """
        Initializes the PrintFirstN class.
        Args:
            n (int): The number of elements to print.
        """
        self.n = n
        self.count = 0

    def process(self, element):
        """
        Processes each element and prints it if count is less than N.
        Args:
            element: The element to process.

        Yields:
            The input element if count is less than N.
        """
        if self.count < self.n:
            self.count += 1
            print(element)
            yield element


def normalize_pokemon(pokemon):
    """
    Converts the given Pokemon heght and weight:
        - dm -> m
        - hg -> kg
    Args:
        pokemon (dict): A dictionary containing Pokemon details.

    Returns:
        dict: The normalized Pokemon data.
    """

    pokemon['height'] = pokemon['height'] / 10.0    
    pokemon['weight'] = pokemon['weight'] / 10.0
    
    return pokemon


def calculate_bmi(pokemon):
    """
    Calculates the BMI for the given Pokemon.
    Args:
        pokemon (dict): A dictionary containing Pokemon details.

    Returns:
        dict: The Pokemon data with BMI added.
    """

    bmi = pokemon['weight'] / (pokemon['height'] ** 2)    
    bmi = round(bmi, 2)
    pokemon['bmi'] = bmi
    
    return pokemon


def run_pipeline():
    """
    Reads Pokemon data from a JSON file, normalizes it, calculates BMI,
    and prints the first 50 rows using Apache Beam.

    This function orchestrates the data processing pipeline using Apache Beam.
    It reads Pokemon data from a JSON file, normalizes it by converting height
    from decimetres to meters and weight from hectograms to kilograms, calculates
    BMI for each Pokemon, and finally prints the details of the first 50 Pokemon
    along with their calculated BMI values.

    Note:
        This function assumes the existence of a 'pokemon_details.json' file in
        the current directory containing the Pokemon data in JSON format.

    Raises:
        FileNotFoundError: If the 'pokemon_details.json' file is not found.
    
    Note 2:
        Execution of the task_1_data_extraction.py will provide a JSON file with desired content.
        This will allow the execution of this script.
    """

    with open('pokemon_details.json', 'r') as file:
        pokemon_data = json.load(file)
    
    normalized_data = [normalize_pokemon(p) for p in pokemon_data]
    
    with beam.Pipeline() as pipeline:
        transformed_data = (
            pipeline
            | 'Create PCollection' >> beam.Create(normalized_data)
            | 'Calculate BMI' >> beam.Map(calculate_bmi)
            | 'Print First 50 Rows' >> beam.ParDo(PrintFirstN(50))
        )


if __name__ == '__main__':
    run_pipeline()
