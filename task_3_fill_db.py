import sqlite3
import json


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
    - data: Dictionary containing Pokemon data withh keys as Pokemon IDs.
    Returns:
    NOne
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
    connection = sqlite3.connect('pokemon.db')
    create_pokemon_table_if_not_exists(connection)

    with open('pokemon_details.json', 'r') as file:
        pokemon_data = json.load(file)
        load_pokemon_data_into_db(connection, pokemon_data)

    connection.close()

if __name__ == '__main__':
    main()
