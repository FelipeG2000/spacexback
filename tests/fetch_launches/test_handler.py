from unittest.mock import patch, MagicMock

from aws_lambda.fetch_launches.fetch_launches import fetch_launches_handler, get_status


@patch("aws_lambda.fetch_launches.fetch_launches.save_launch")
@patch("aws_lambda.fetch_launches.fetch_launches.get_launchpad_name")
@patch("aws_lambda.fetch_launches.fetch_launches.get_rocket_name")
@patch("aws_lambda.fetch_launches.fetch_launches.fetch_launches")
def test_lambda_handler_success(mock_fetch, mock_get_rocket_name, mock_get_launchpad_name, mock_save_launch):
    # Mock SpaceX data
    mock_fetch.return_value = [{
        "id": "abc123",
        "name": "Test Mission",
        "rocket": "rocket_123",
        "date_utc": "2025-01-01T00:00:00Z",
        "success": True,
        "upcoming": False,
        "details": None,
        "launchpad": "Pad-1",
        "links": {
            "webcast": None,
            "patch": {"small": None}
        }
    }]
    mock_get_rocket_name.return_value = "Falcon 9"
    mock_get_launchpad_name.return_value = "Launch Complex 39A"

    response = fetch_launches_handler({}, {})

    assert response["statusCode"] == 200
    assert "1 launches processed successfully" in response["body"]
    mock_save_launch.assert_called_once()

def test_get_status_upcoming():
    launch = {"upcoming": True}
    assert get_status(launch) == "upcoming"

def test_get_status_success():
    launch = {"upcoming": False, "success": True}
    assert get_status(launch) == "success"

def test_get_status_failed():
    launch = {"upcoming": False, "success": False}
    assert get_status(launch) == "failed"

@patch("aws_lambda.fetch_launches.fetch_launches.save_launch")
@patch("aws_lambda.fetch_launches.fetch_launches.get_launchpad_name")
@patch("aws_lambda.fetch_launches.fetch_launches.get_rocket_name")
@patch("aws_lambda.fetch_launches.fetch_launches.fetch_launches")
def test_lambda_handler_ignores_launch_without_id(mock_fetch, mock_get_rocket_name, mock_get_launchpad_name, mock_save_launch):
    mock_fetch.return_value = [
        {
            "id": "abc123",
            "name": "Test Mission A",
            "rocket": "rocket_a",
            "date_utc": "2025-01-01T00:00:00Z",
            "success": True,
            "upcoming": False,
            "details": None,
            "launchpad": "Pad-1",
            "links": {"webcast": None, "patch": {"small": None}}
        },
        {
            # No 'id', should ignore it
            "name": "Invalid Mission",
            "rocket": "rocket_x"
        },
        {
            "id": "def456",
            "name": "Test Mission B",
            "rocket": "rocket_b",
            "date_utc": "2025-01-02T00:00:00Z",
            "success": False,
            "upcoming": False,
            "details": None,
            "launchpad": "Pad-2",
            "links": {"webcast": None, "patch": {"small": None}}
        }
    ]
    mock_get_rocket_name.return_value = "Falcon 9"
    mock_get_launchpad_name.return_value = "Launch Complex 40"

    response = fetch_launches_handler({}, {})

    assert response["statusCode"] == 200
    assert "2 launches processed successfully" in response["body"]
    assert mock_save_launch.call_count == 2