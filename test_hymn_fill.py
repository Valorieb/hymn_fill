import unittest
from unittest.mock import MagicMock, patch
from selenium.webdriver.support import expected_conditions as EC
from hymn_fill import get_hymn_info, get_hymn_dict, save_hymns_to_json

class TestHymnScraper(unittest.TestCase):

    def test_get_hymn_info(self):
        mock_driver = MagicMock()
        mock_driver.get = MagicMock()
        mock_driver.find_elements.return_value =[
            MagicMock(text="1. The Morning Breaks"),
            MagicMock(text="2. The Spirit of God")
        ]

        hymn_info_list = get_hymn_info(mock_driver)
        print(hymn_info_list)

        self.assertEqual(len(hymn_info_list), 4)
        self.assertEqual(hymn_info_list[0], "1. The Morning Breaks")
        self.assertEqual(hymn_info_list[1], "2. The Spirit of God")
        self.assertEqual(hymn_info_list[2], "1. The Morning Breaks")  # From second URL
        self.assertEqual(hymn_info_list[3], "2. The Spirit of God")   # From second URL

        mock_driver.quit.assert_called_once()

    def test_get_hymn_dict(self):
       
        mock_get_hymn_info = MagicMock(return_value=[
            "1. The Morning Breaks",
            "2. The Spirit of God"
        ])

        with unittest.mock.patch('hymn_fill.get_hymn_info', mock_get_hymn_info):
            hymn_dict = get_hymn_dict()

        print(f"HYMN DICTIONARY: {hymn_dict}")

        self.assertEqual(len(hymn_dict), 2)
        self.assertEqual(hymn_dict["1"], "The Morning Breaks")
        self.assertEqual(hymn_dict["2"], "The Spirit of God")

    @patch('hymn_fill.get_hymn_dict')
    @patch('json.dump')

    def test_save_hymns_to_json(self, mock_json_dump, mock_get_hymn_dict):

        mock_get_hymn_dict.return_value = {
            "1": "The Morning Breaks",
            "2": "The Spirit of God",
            "302": "I Know My Father Lives",
            "1017": "This Is the Christ"
        }

        save_hymns_to_json()

        # Assert that json.dump was called with the correct arguments
        mock_json_dump.assert_called_once_with(
            {
                "1": "The Morning Breaks",
                "2": "The Spirit of God",
                "302": "I Know My Father Lives",
                "1017": "This Is the Christ"
            },
            unittest.mock.ANY,  # The file handler
            indent=4
        )

        # Assert that get_hymn_dict was called once
        mock_get_hymn_dict.assert_called_once()

        # Ensure the number of hymns in the saved dictionary matches the expected count
        self.assertEqual(len(mock_get_hymn_dict.return_value), 4)

        # Verify that a specific key-value pair exists in the dictionary
        self.assertIn("302", mock_get_hymn_dict.return_value)
        self.assertEqual(mock_get_hymn_dict.return_value["302"], "I Know My Father Lives")

if __name__ == "__main__":
    unittest.main()

