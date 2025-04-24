"""Lambda function to delete an inventory item from DynamoDB."""

import json
import boto3


def lambda_handler(event, context):
    """
    Handle DELETE request to remove an inventory item by ID.
    Expects 'id' in the path parameters.
    """
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter.")
        }

    item_id = event["pathParameters"]["id"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        table.delete_item(Key={"item_id": item_id})
        return {
            "statusCode": 200,
            "body": json.dumps(f"Item {item_id} deleted successfully.")
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(str(e))
        }