"""Lambda function to retrieve all inventory items from DynamoDB."""

import json
import boto3


def lambda_handler(event, context):
    """
    Handle GET request to retrieve all inventory items.
    Returns a list of all items in the Inventory table.
    """
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        response = table.scan()
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
