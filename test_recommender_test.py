import unittest
from utils.recommender import recommendation_engine
from main import process_csv_files

# Adding important tests
class TestListFiles(unittest.TestCase):
    def test_process_csv_files(self):
        response_length = 49
        response = process_csv_files()
        self.assertEqual(len(response), response_length)

class RecommendationEngine(unittest.TestCase):
    def test_recommender_returns_none(self):
        response = recommendation_engine('', '', '', '')
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()