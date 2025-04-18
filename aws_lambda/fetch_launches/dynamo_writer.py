import boto3

dynamodb = boto3.client("dynamodb")
TABLE_NAME = "SpaceXLaunchesDB"

def save_launch(item):
    dynamodb.put_item(TableName=TABLE_NAME, Item=item)
