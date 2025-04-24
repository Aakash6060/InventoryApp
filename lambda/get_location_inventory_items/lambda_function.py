"""Lambda function to retrieve all inventory items for a specific location ID."""

import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """
    Handle GET request to retrieve items by location ID.
    Expects 'id' in path parameters.
    """
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter.")
        }

    location_id = int(event["pathParameters"]["id"])
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        response = table.query(
            IndexName="LocationIndex",
            KeyConditionExpression=Key("location_id").eq(location_id)
        )
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }
