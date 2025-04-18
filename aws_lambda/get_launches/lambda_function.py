import json
from dynamo_reader import get_latest_launches

def lambda_handler(event, context):
    try:
        launches = get_latest_launches(limit=10)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(launches)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
