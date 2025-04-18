import pytest
from unittest.mock import patch
import requests

from aws_lambda.fetch_launches import spacex
from aws_lambda.fetch_launches.spacex import get_rocket_name


@patch("requests.get")
def test_get_rocket_name_success(mock_get):
    spacex.rocket_cache.clear()
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"name": "Falcon 9"}
    name = get_rocket_name("test_id")
    assert name == "Falcon 9"

@patch("requests.get")
def test_fetch_launches_failure(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("Error")
    with pytest.raises(requests.HTTPError):
        spacex.fetch_launches()