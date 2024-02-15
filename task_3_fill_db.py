import sqlite3
import json
import os


def create_pokemon_table_if_not_exists(connection):
    """
    Create the 'pokemon_data' table in the database if it does not already exist.
    Args:
    - connection: SQLite database connection object.
    Returns:
    None
    """
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            height REAL,
            weight REAL,
            bmi REAL
        )
    ''')
    connection.commit()
    cursor.close()


def load_pokemon_data_into_db(connection, data):
    """
    Load Pokemon data into the 'pokemon_data' table in the database
    
    Args:
    - connection: SQLite database connection object
    - data: Dictionary containing Pokemon data with keys as Pokemon IDs.
    Returns:
    None
    """
    cursor = connection.cursor()
    for pokemon_id, details in data.items():
        name = details['name']
        height = details['height']
        weight = details['weight']
        bmi = details['bmi']
        try:
            cursor.execute('''
                INSERT INTO pokemon_data (id, name, height, weight, bmi)
                VALUES (?, ?, ?, ?, ?)
            ''', (pokemon_id, name, height, weight, bmi))
        except sqlite3.IntegrityError as e:
            print(f"Skipping insertion for Pokemon ID {pokemon_id}. Error: {e}")
    connection.commit()
    cursor.close()


def main():
    """
    Main function to load Pokemon data into the db
    """

    json_file_path = 'pokemon_details.json'
    if not os.path.exists(json_file_path):
        print(f"Error: JSON file '{json_file_path}' not found.")
        return
    connection = sqlite3.connect('pokemon.db')

    try:
        create_pokemon_table_if_not_exists(connection)

        with open(json_file_path, 'r') as file:
            pokemon_data = json.load(file)
            load_pokemon_data_into_db(connection, pokemon_data)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        connection.close()


if __name__ == '__main__':
    main()
