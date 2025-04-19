import pytest
from unittest.mock import patch, MagicMock
import requests
from aws_lambda.fetch_launches import spacex
from aws_lambda.fetch_launches.spacex import (
    fetch_launches,
    get_rocket_name,
    get_launchpad_name,
    rocket_cache,
    launchpad_cache
)


# Helper function to reset caches between tests
@pytest.fixture(autouse=True)
def clear_caches():
    rocket_cache.clear()
    launchpad_cache.clear()


# Tests for fetch_launches()
@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_fetch_launches_success(mock_get):
    """Test successful fetch of launches"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": "1", "name": "Test Launch"}]
    mock_get.return_value = mock_response

    result = fetch_launches()
    assert result == [{"id": "1", "name": "Test Launch"}]
    mock_get.assert_called_once_with("https://api.spacexdata.com/v4/launches")


@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_fetch_launches_failure(mock_get):
    """Test failed fetch of launches"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("API Error")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        fetch_launches()


# Tests for get_rocket_name()
@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_get_rocket_name_success(mock_get):
    """Test successful rocket name fetch"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Falcon 9"}
    mock_get.return_value = mock_response

    name = get_rocket_name("falcon9")
    assert name == "Falcon 9"
    mock_get.assert_called_once_with("https://api.spacexdata.com/v4/rockets/falcon9")


@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_get_rocket_name_cache(mock_get):
    """Test rocket name cache hit"""
    rocket_cache["falcon9"] = "Falcon 9 (cached)"

    name = get_rocket_name("falcon9")
    assert name == "Falcon 9 (cached)"
    mock_get.assert_not_called()


def test_get_rocket_name_empty_id():
    """Test empty rocket ID"""
    name = get_rocket_name("")
    assert name == "Unknown"


@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_get_rocket_name_failure(mock_get):
    """Test failed rocket name fetch"""
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("Not Found")
    mock_get.return_value = mock_response

    name = get_rocket_name("unknown_rocket")
    assert name == "ID: unknown_rocket"


# Tests for get_launchpad_name()
@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_get_launchpad_name_success(mock_get):
    """Test successful launchpad name fetch"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"name": "Kennedy Space Center"}
    mock_get.return_value = mock_response

    name = get_launchpad_name("ksc")
    assert name == "Kennedy Space Center"
    mock_get.assert_called_once_with("https://api.spacexdata.com/v4/launchpads/ksc")


@patch("aws_lambda.fetch_launches.spacex.requests.get")
def test_get_launchpad_name_cache(mock_get):
    """Test launchpad name cache hit"""
    launchpad_cache["ksc"] = "Kennedy (cached)"

    name = get_launchpad_name("ksc")
    assert name == "Kennedy (cached)"
    mock_get.assert_not_called()


def test_get_launchpad_name_empty_id():
    """Test empty launchpad ID"""
    name = get_launchpad_name("")
    assert name == "Unknown"
