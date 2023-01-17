import unittest

from plugin import match_field_name

class PluginTest(unittest.TestCase):
    def test_match_field_name(self):
        fake_api_to_fields = {
            "car": ["red", "white", "black"],
            "book": ["chapter", "author"],
            "movie": ["duration", "producer"]
        }
        fake_patterns = ["red", "chapter"]
        expected = {
            "car": set(["red"]),
            "book": set(["chapter"])
        }
        self.assertDictEqual(match_field_name(fake_api_to_fields, fake_patterns), expected)

    def test_match_field_name_empty(self):
        fake_api_to_fields = {
            "car": ["red", "white", "black"],
            "book": ["chapter", "author"],
            "movie": ["duration", "producer"]
        }
        fake_patterns = ["not_there"]
        expected = {}
        self.assertDictEqual(match_field_name(fake_api_to_fields, fake_patterns), expected)
    
    def test_match_field_name_empty_args(self):
        fake_api_to_fields = {}
        fake_patterns = []
        expected = {}
        self.assertDictEqual(match_field_name(fake_api_to_fields, fake_patterns), expected)

    def test_match_field_name_empty_pattern(self):
        fake_api_to_fields = {
            "car": ["red", "white", "black"],
            "book": ["chapter", "author"],
            "movie": ["duration", "producer"]
        }
        fake_patterns = []
        expected = {}
        self.assertDictEqual(match_field_name(fake_api_to_fields, fake_patterns), expected)
