import boto3

TABLE_NAME = "SpaceXLaunches"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def get_latest_launches(limit=10):
    # Warning: scan is inefficient at scale
    response = table.scan(Limit=100)
    items = response.get("Items", [])
    sorted_items = sorted(items, key=lambda x: x.get("launch_date", ""), reverse=True)
    return sorted_items[:limit]
