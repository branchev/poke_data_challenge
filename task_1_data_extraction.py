import requests
import asyncio
import json
import aiohttp


# Error message for failed API requests
error_message ='Failed to retrieve pokemon details from API'


async def fetch_pokemon_details(session, url):
    """
    Fetches details of a Pokemo from the given URL asynchronously.

    Args:
        session (aiohttp.ClientSession): An aiohttp ClientSession obj for making HTTP requests.
        url (str): The URL of the Pokemon details API endpoint

    Returns:
        dict: A dicionary containing the details of the pokemon, including its ID, name, height, and weight.
              Returns None if an error occures upon fetching the details
    """

    async with session.get(url) as response:
        try:
            response.raise_for_status()
            data = await response.json()
            return {
                'id': data['id'],
                'name': data['name'],
                'height': data['height'],
                'weight': data['weight']
            }
        except Exception as e:
            print(f'{error_message}: {e}')
            return None


async def fetch_pokemon_details_batch(pokemon_urls):
    """
    Fetches details of Multiple Pokemon asynchronously
    Args:
        pokemon_urls (list): a list of URLs for the Pokemon details API endpoints
    Returns:
        list: A list of dictionaries containing the details of Pokemon
              Each dictionary includes the ID, name, height, and weight.
    """

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon_details(session, url) for url in pokemon_urls]
        return await asyncio.gather(*tasks)


TYPE_ID = 3
LIMIT_COUNT = 50
api_url = f'https://pokeapi.co/api/v2/type/{TYPE_ID}/?limit={LIMIT_COUNT}'

try:
    response = requests.get(api_url)
    response.raise_for_status()

    data = response.json()
    # The line below is commented because of pagination with 'limit' does not works to this endpoint!!!!
    # pokemon_results = data['pokemon']
    pokemon_results = data['pokemon'][:LIMIT_COUNT]
    pokemon_urls = [pokemon['pokemon']['url'] for pokemon in pokemon_results]

    loop = asyncio.get_event_loop()
    pokemon_details_list = loop.run_until_complete(fetch_pokemon_details_batch(pokemon_urls))

    for idx, pokemon_details in enumerate(pokemon_details_list, start=1):
        if pokemon_details:
            print(f"{idx}: {pokemon_details['name']} - "
                    f"ID: {pokemon_details['id']}, "
                    f"Height: {pokemon_details['height']}, "
                    f"Weight: {pokemon_details['weight']}"
                )

    with open('pokemon_details.json', 'w') as file:
        json.dump([details for details in pokemon_details_list if details], file, indent=4)

except Exception as e:
    print(f'{error_message}: {e}')
