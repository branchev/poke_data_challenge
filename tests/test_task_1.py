import unittest
import aiohttp
from aiohttp.test_utils import unittest_run_loop
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from unittest.mock import patch, MagicMock
from task_1_data_extraction import fetch_pokemon_details, fetch_pokemon_details_batch


class TestPokemonAPI(AioHTTPTestCase):
    """Test case for testing Pokemon API."""

    async def get_application(self):
        """Get the application instance."""
        return self.app

    async def setUpAsync(self):
        """Set up method called before running the test."""
        self.pokemon_data = {
            'id': 1,
            'name': 'pokemon',
            'height': 7,
            'weight': 69
        }
        self.pokemon_url = '/api/v2/pokemon/1/'
        self.app = web.Application()
        self.app.router.add_get(self.pokemon_url, self.fake_pokemon_details)
        await super().setUpAsync()

    async def fake_pokemon_details(self, request):
        """Fake method to return Pokemon details."""
        return web.json_response(self.pokemon_data)
    
    @unittest_run_loop
    async def test_fetch_pokemon_details(self):
        """Test fetching Pokemon details."""
        async with self.client.get(self.pokemon_url) as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()
            self.assertEqual(data, self.pokemon_data)

    @patch('task_1_data_extraction.fetch_pokemon_details', return_value=None)
    async def test_fetch_pokemon_details_batch(self, mock_fetch):
        """Test fetching batch of Pokemon details."""
        pokemon_urls = [self.pokemon_url]
        results = await fetch_pokemon_details_batch(pokemon_urls)
        self.assertIsNone(results[0])

    @unittest_run_loop
    async def test_fetch_pokemon_details_successful(self):
        """Test successful fetching of Pokemon details."""
        async with self.client.get(self.pokemon_url) as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()
            self.assertEqual(data, self.pokemon_data)

    @patch('task_1_data_extraction.fetch_pokemon_details', return_value=None)
    async def test_fetch_pokemon_details_successful_mocked(self, mock_fetch):
        """Test successful fetching of Pokemon details with mocking."""
        mock_response_data = {'id': 1, 'name': 'pokemon', 'height': 7, 'weight': 69}
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data

        async with self.client.get(self.pokemon_url) as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()
            self.assertEqual(data, mock_response_data)

    @patch('task_1_data_extraction.aiohttp.ClientSession.get')
    @unittest_run_loop
    async def test_fetch_pokemon_details_error(self, mock_get):
        """Test handling error while fetching Pokemon details."""
        mock_get.side_effect = aiohttp.ClientError()

        async with aiohttp.ClientSession() as session:
            pokemon_details = await fetch_pokemon_details(session, 'https://fake-pokemon-api.com/1')

        self.assertIsNone(pokemon_details)

    async def tearDownAsync(self):
        """Tear down method called after running the test."""
        await super().tearDownAsync()
        if hasattr(self, 'client') and self.client:
            await self.client.close()

if __name__ == '__main__':
    unittest.main()
