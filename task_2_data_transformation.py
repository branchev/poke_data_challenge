import json
import apache_beam as beam


def normalize_pokemon(pokemon):
    """
    Converts the given Pokemon height and weight:
        - dm -> m
        - hg -> kg
    Args:
        pokemon (dict): A dictionary containing Pokemon details.

    Returns:
        dict: The normalized Pokemon data.
    """
    pokemon['height'] = round(pokemon['height'] / 10.0, 2)
    pokemon['weight'] = round(pokemon['weight'] / 10.0, 2)
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


def update_json_file(pokemon_data):
    """
    Updates the JSON file with the modified Pokemon data.
    Args:
        pokemon_data (dict): A dictionary containing the modified Pokemon data.
    """
    pokemon_id, updated_data = pokemon_data
    try:
        with open('pokemon_details.json', 'r+') as file:
            data = json.load(file)
            data[pokemon_id] = updated_data
            file.seek(0)
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print("Error: JSON file 'pokemon_details.json' not found.")
    except Exception as e:
        print(f"An error occurred while updating the JSON file: {e}")


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
        ValueError: If the 'bmi' key already exists in the Pokemon data.
    
    Note 2:
        Execution of the task_1_data_extraction.py will provide a JSON file with desired content.
        This will allow the execution of this script.
    """
    try:
        with open('pokemon_details.json', 'r') as file:
            pokemon_data = json.load(file)
            # Checking if 'bmi' key exists - the data is already transformed once
            if 'bmi' in pokemon_data[next(iter(pokemon_data))]:
                raise ValueError("BMI already calculated and data is updated. Pipeline cannot proceed.")

        with beam.Pipeline() as pipeline:
            transformed_data = (
                pipeline
                | 'Read JSON File' >> beam.Create(pokemon_data.items())
                | 'Normalize Pokemon Data' >> beam.Map(lambda kv: (kv[0], normalize_pokemon(kv[1])))
                | 'Calculate BMI' >> beam.Map(lambda kv: (kv[0], calculate_bmi(kv[1])))
                | 'Update JSON' >> beam.Map(update_json_file)
            )

    except FileNotFoundError:
        print("Error: JSON file 'pokemon_details.json' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def print_pokemon_details():
    """
    Prints the Pokemon details
    """
    try:
        with open('pokemon_details.json', 'r') as file:
            pokemon_data = json.load(file)

        for index, (pokemon_id, details) in enumerate(pokemon_data.items(), start=1):
            print(f"{index}: {details['name'].capitalize()} - "
                  f"ID: {pokemon_id}, "
                  f"Height: {details['height']:.2f} m., "
                  f"Weight: {details['weight']:.2f} kg., "
                  f"BMI: {details['bmi']:.2f}")
    except FileNotFoundError:
        print("Error: JSON file 'pokemon_details.json' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    run_pipeline()
    print_pokemon_details()
