# PokéData Challenge: Unleash the Power of Python and Apache Beam

Welcome to the "PokéData Processing Challenge: Unleash the Power of Python and Apache Beam"! This assessment evaluates your proficiency in Python programming and data processing using Apache Beam. In this challenge, you will leverage the PokéAPI (https://pokeapi.co) to extract information about Pokémon, transform the data using Apache Beam, and load it into an SQLite database. Additionally, you will showcase your advanced data processing skills by implementing an extra feature.

## INSTALLATION

This project requires Python 3.7 or higher and assumes installation on Ubuntu 18.04+ or similar Debian based GNU/Linux distribution.

### System Requirements

##### Base

Before running the project, make sure you have the following installed:

Python 3.7 or higher
Pip
SQLite

### SQLite Database Installation

Add necessary repositories:
    
    To install the SQLite command-line interface on Ubuntu, first update your package list:

    $ sudo apt update

    Now install SQLite:

    $ sudo apt install sqlite3

    To verify the installation, check the software’s version:

    $ sqlite3 --version


## Setting Up the Environment

### 1. Clone the repository to your local machine:

    $ git clone <repository_url>

### 2. Navigate to the project directory:

    $ cd poke_data_challenge

### 3. Create a virtual environment:

    $ python3 -m venv venv

### 4. Activate the virtual environment:

    $ source venv/bin/activate

### 5. Install the required packages using pip:

    $ pip install -r requirements.txt


### Running Tests
To ensure that all tests pass, run the following command:

    $ python -m unittest discover -s tests -v

## EXECUTE THE PROJECT

To execute the project functionality fllow you must follow a strict sequence in the execution of the processes as described below:

### Task 1: Data Extraction

Retrieving data from the PokéAPI to get information about a set of Pokémon (use this set: type/3). Extracting id, name, height, and weight for the first 50 Pokémon. Print the extracted details and save the results into a file format that can be processed in the next task.

    $ python task_1_data_extraction.py

### Task 2: Data Transformation with Apache Beam

A data transformation pipeline using Apache Beam to perform the following tasks on the extracted Pokémon data:

- Convert the height and weight attributes to meters and kilograms, respectively.
- Create a new column called bmi (Body Mass Index) using the formula: bmi = weight / (height^2). Round the result to two decimal places.
- Print the first 50 rows of the transformed dataset.


    `$ python task_2_data_transformation.py`


### Task 3: Data Loading

Load the transformed Pokémon data into an SQLite database.

    $ python task_3_fill_db.py

### Task 4: Data Processing

It shows some metrics compiled using the information available in the database:

- Calculate average BMI
- Find Pokemon with highest BMI
- Analize height-weight ratio
- Classify weight category


    `$ python task_4_advanced_data_processing.py` 

