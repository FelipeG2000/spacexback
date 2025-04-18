from unittest.mock import patch, MagicMock
from aws_lambda.get_launches.dynamo_reader import get_latest_launches

@patch("aws_lambda.get_launches.dynamo_reader.table")
def test_get_latest_launches_returns_sorted_limited(mock_table):
    # Fake unsorted DynamoDB response
    mock_table.scan.return_value = {
        "Items": [
            {"launch_date": "2023-01-01", "mission": "A"},
            {"launch_date": "2024-05-05", "mission": "B"},
            {"launch_date": "2022-10-10", "mission": "C"},
        ]
    }

    result = get_latest_launches(limit=2)

    assert len(result) == 2
    assert result[0]["launch_date"] == "2024-05-05"
    assert result[1]["launch_date"] == "2023-01-01"
