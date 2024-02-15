import sqlite3
import numpy as np
import os


def calculate_average_bmi(connection):
    """
    Calculate the average BMI of all Pokémon stored in the database.
    
    Args:
        connection: SQLite database connection object.
    
    Returns:
        float: Average BMI of all Pokémon.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT AVG(bmi) FROM pokemon_data')
        average_bmi = cursor.fetchone()[0]
        cursor.close()
        return average_bmi
    except sqlite3.Error as e:
        print(f"Error while calculating average BMI: {e}")
        return None


def find_pokemon_with_highest_bmi(connection):
    """
    Find the Pokémon with the highest BMI stored in the database.
    
    Args:
        connection: SQLite database connection object.
    
    Returns:
        str: Name of the Pokémon with the highest BMI.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM pokemon_data WHERE bmi = (SELECT MAX(bmi) FROM pokemon_data)')
        pokemon_name = cursor.fetchone()[0]
        cursor.close()
        return pokemon_name
    except sqlite3.Error as e:
        print(f"Error while finding Pokémon with highest BMI: {e}")
        return None


def analyze_height_weight_ratio(connection):
    """
    Analyze the height-weight ratio of all Pokémon stored in the database.
    Calculates the average height, average weight, and correlation coefficient between height and weight.
    
    Args:
        connection: SQLite database connection object.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT AVG(height), AVG(weight) FROM pokemon_data')
        average_height, average_weight = cursor.fetchone()
        print(f"Average Height: {average_height:.2f}")
        print(f"Average Weight: {average_weight:.2f}")

        cursor.execute('SELECT height, weight FROM pokemon_data')
        heights, weights = zip(*cursor.fetchall())

        correlation_coefficient = np.corrcoef(heights, weights)[0, 1]
        print(f"Correlation Coefficient (Height-Weight): {correlation_coefficient:.2f}")

        cursor.close()
    except sqlite3.Error as e:
        print(f"Error while analyzing height-weight ratio: {e}")


def classify_weight_category(weight):
    """
    Classify the weight category based on the weight of the Pokémon.
    
    Args:
        weight: Weight of the Pokémon.
    
    Returns:
        str: Weight category ('Light', 'Medium', or 'Heavy').
    """
    if weight < 50:
        return "Light"
    elif 50 <= weight < 100:
        return "Medium"
    else:
        return "Heavy"


def assign_weight_categories(connection):
    """
    Assign weight categories to all Pokémon stored in the database and print the results.
    
    Args:
        connection: SQLite database connection object.
    """
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT name, weight FROM pokemon_data')
        for name, weight in cursor.fetchall():
            weight_category = classify_weight_category(weight)
            print(f"{name}: {weight_category}")
        cursor.close()
    except sqlite3.Error as e:
        print(f"Error while assigning weight categories: {e}")


def main():
    """
    Main function to execute the analysis and classification of Pokemon data stored in the SQLite database.

    This function orchestrates the process of connecting to the SQLite database,
    performing various analyses on the data, and classifying Pokémon
    based on their weight categories. It calculates the average BMI of all Pokémon,
    finds the Pokémon with the highest BMI, analyzes the height-weight ratio,
    and assigns weight categories to each Pokémon. Error handling is implemented
    to gracefully handle potential exceptions during database operations.

    Returns:
        None
    """
    db_file = 'pokemon.db'
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"SQLite database file '{db_file}' not found.")

    try:
        connection = sqlite3.connect(db_file)

        average_bmi = calculate_average_bmi(connection)
        if average_bmi is not None:
            print(f"Average BMI of all Pokémon: {average_bmi:.2f}")

        pokemon_with_highest_bmi = find_pokemon_with_highest_bmi(connection)
        if pokemon_with_highest_bmi is not None:
            print(f"Pokémon with the highest BMI: {pokemon_with_highest_bmi}")

        analyze_height_weight_ratio(connection)
        assign_weight_categories(connection)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        connection.close()


if __name__ == '__main__':
    main()
