from spacex import fetch_launches, get_rocket_name, get_launchpad_name
from dynamo_writer import save_launch
import json

def fetch_launches_handler(event, context):
    launches = fetch_launches()
    count = 0

    for launch in launches:
        launch_id = launch.get("id")
        if not launch_id:
            continue

        rocket_name = get_rocket_name(launch.get("rocket", ""))
        launchpad_name = get_launchpad_name(launch.get("launchpad", ""))
        item = {
            "launch_id": {"S": launch_id},
            "mission_name": {"S": launch.get("name", "Unknown")},
            "rocket_name": {"S": rocket_name},
            "launch_date": {"S": launch.get("date_utc", "Unknown")},
            "status": {"S": get_status(launch)},
            "launchpad_name": {"S": launchpad_name},
            "upcoming": {"BOOL": launch.get("upcoming", False)},
            "details": {"S": launch.get("details") or "No details"},
            "webcast": {"S": launch.get("links", {}).get("webcast") or "N/A"},
            "patch_image": {"S": launch.get("links", {}).get("patch", {}).get("small") or "N/A"}
        }

        save_launch(item)
        count += 1

    return {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "*"
        },
    "body": json.dumps({
        "message": f"{count} launches processed successfully."
        })
    }


def get_status(launch):
    if launch.get("upcoming"):
        return "upcoming"
    if launch.get("success"):
        return "success"
    return "failed"
