#!/usr/bin/env python3

"""Unit tests for the utils module functions."""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from typing import Mapping, Sequence, Any
from unittest.mock import patch, Mock
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test suite for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test that access_nested_map returns expected results for given inputs."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),            # Map is empty, path "a" does not exist
        ({"a": 1}, ("a", "b")),  # Map has "a", but "b" under "a" does not
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence) -> None:
        """Test that access_nested_map raises KeyError with the correct message for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        # Check that the KeyError message matches the missing key
        self.assertEqual(str(context.exception), repr(path[-1])) 

class TestGetJson(unittest.TestCase):
    """Test suite for the get_json function."""

    @unittest.mock.patch('requests.get')
    def test_get_json(self, mock_get: Mock) -> None:
        """Test that get_json returns the expected payload and calls requests.get correctly."""
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]

        calls = []
        for test_url, test_payload in test_cases:
            # Create a mock response object
            mock_response = Mock()
            # Set the return value of the json() method of the mock response
            mock_response.json.return_value = test_payload
            # Set the return value of the mock get to be this mock response
            mock_get.return_value = mock_response

            # Call get_json with the test URL
            result = get_json(test_url)

            # Ensure requests.get was called with the current test_url
            mock_get.assert_called_with(test_url)
            calls.append(unittest.mock.call(test_url))

            # Verify the result matches the expected payload
            self.assertEqual(result, test_payload)

        # Ensure requests.get was called the correct number of times with the correct URLs
        self.assertEqual(mock_get.call_count, len(test_cases))
        mock_get.assert_has_calls(calls, any_order=True) # Use any_order=True

if __name__ == "__main__":
    unittest.main()