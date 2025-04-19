import json
from dynamo_reader import get_latest_launches

def handle_get_launches(event, context):
    try:
        query_params = event.get("queryStringParameters") or {}
        limit_param = query_params.get("limit")

        limit = int(limit_param) if limit_param is not None else None

        launches = get_latest_launches(limit=limit)
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
