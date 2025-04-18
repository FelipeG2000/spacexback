from unittest.mock import patch
from aws_lambda.get_launches.get_launches import handle_get_launches

@patch("aws_lambda.get_launches.get_launches.get_latest_launches")
def test_lambda_handler_success(mock_get_latest):
    mock_get_latest.return_value = [{"mission": "Test"}]

    response = handle_get_launches({}, {})
    assert response["statusCode"] == 200
    assert "Test" in response["body"]

@patch("aws_lambda.get_launches.get_launches.get_latest_launches")
def test_lambda_handler_error_handling(mock_get_latest):
    mock_get_latest.side_effect = Exception("Something failed")

    response = handle_get_launches({}, {})
    assert response["statusCode"] == 500
    assert "error" in response["body"]
