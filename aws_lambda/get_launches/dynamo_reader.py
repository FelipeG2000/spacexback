import boto3

TABLE_NAME = "SpaceXLaunchesDB"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def get_latest_launches(limit=None):
    response = table.scan()
    items = response.get("Items", [])
    sorted_items = sorted(items, key=lambda x: x.get("launch_date", ""), reverse=True)

    if limit is not None:
        return sorted_items[:limit]
    return sorted_items
