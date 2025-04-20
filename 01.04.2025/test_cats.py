import pytest
from unittest.mock import patch, Mock
import requests
from code_cats import CatFactProcessor, APIError

class TestCatFactProcessor:
    @pytest.fixture
    def processor(self):
        return CatFactProcessor()

    # get_fact func tests
    @patch('requests.get')
    def test_get_fact_success(self, mock_get, processor):
        # mock response
        mock_response = Mock()
        mock_response.json.return_value = {"fact": "Cats are amazing!"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # func call
        result = processor.get_fact()

        assert result == "Cats are amazing!" #true!!!!
        assert processor.last_fact == "Cats are amazing!"
        mock_get.assert_called_once_with("https://catfact.ninja/fact")

    @patch('requests.get')
    def test_get_fact_http_error(self, mock_get, processor):
        # mock response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        # exception test
        with pytest.raises(APIError) as excinfo:
            processor.get_fact()
        assert "API call error" in str(excinfo.value)

    @patch('requests.get')
    def test_get_fact_connection_error(self, mock_get, processor):
        # mock error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

        # exception call test
        with pytest.raises(APIError) as excinfo:
            processor.get_fact()
        assert "API call error" in str(excinfo.value)

    @patch('requests.get')
    def test_get_fact_invalid_json(self, mock_get, processor):
        # mock response with invalid json
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # exception test
        with pytest.raises(APIError) as excinfo:
            processor.get_fact()
        assert "API call error" in str(excinfo.value)

    # get_fact_analysis() test
    def test_get_fact_analysis_empty(self, processor):
        processor.last_fact = ""
        result = processor.get_fact_analysis()
        assert result == {"length": 0, "letter_frequencies": {}}

    def test_get_fact_analysis_with_fact(self, processor):
        processor.last_fact = "Test fact 123"
        result = processor.get_fact_analysis()
        
        assert result["length"] == 12
        assert result["letter_frequencies"] == {
            't': 3, 'e': 1, 's': 1, ' ': 2, 
            'f': 1, 'a': 1, 'c': 1, '1': 1, '2': 1, '3': 1
        }

    def test_get_fact_analysis_case_insensitive(self, processor):
        processor.last_fact = "AaBbCc"
        result = processor.get_fact_analysis()
        assert result["letter_frequencies"] == {'a': 2, 'b': 2, 'c': 2}

    def test_get_fact_analysis_special_chars(self, processor):
        processor.last_fact = "Hello, world!"
        result = processor.get_fact_analysis()
        assert result["letter_frequencies"][','] == 1
        assert result["letter_frequencies"]['!'] == 1

