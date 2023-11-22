import app
import unittest
import requests
import json
from unittest.mock import patch, MagicMock

class TestGifSearchService(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    # Testing successful search of gifs
    @patch('requests.get')
    def test_successful_retrieval_of_gifs(self, mock_get):
        
        mock_response = MagicMock()
        mock_get.json.return_value = {
            "data": [
                {
                    "gif_id": "SggILpMXO7Xt6", 
                    "url": "https://example.com/gif1.gif"
                }
            ]
        }

        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.app.get('/query?searchTerm=funny')
        self.assertEqual(response.status_code, 200)

    # Testing invalid search term 
    def test_invalid_search_terms(self):
        response = self.app.get('/query?searchTerm=')
        self.assertEqual(response.status_code, 400)

    # Test a non-existent route
    def test_non_existent_route(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()