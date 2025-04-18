from unittest.mock import patch
from aws_lambda.fetch_launches.dynamo_writer import save_launch

@patch("aws_lambda.fetch_launches.dynamo_writer.dynamodb")
def test_save_launch_calls_put_item(mock_dynamodb):
    """
    Unit test to verify that save_launch() calls DynamoDB's put_item
    with the expected parameters.
    """
    # Arrange
    sample_item = {
        "launch_id": {"S": "test123"},
        "mission_name": {"S": "Test Mission"},
        "rocket_name": {"S": "Falcon 9"},
        "launch_date": {"S": "2025-01-01T00:00:00Z"},
        "status": {"S": "success"},
        "launchpad_name": {"S": "Test Site"},
        "upcoming": {"BOOL": False},
        "details": {"S": "Test launch"},
        "webcast": {"S": "N/A"},
        "patch_image": {"S": "N/A"}
    }

    # Act
    save_launch(sample_item)

    # Assert
    mock_dynamodb.put_item.assert_called_once_with(
        TableName="SpaceXLaunchesDB",
        Item=sample_item
    )
