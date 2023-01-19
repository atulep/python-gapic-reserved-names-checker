# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 		https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
