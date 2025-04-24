"""Lambda function to retrieve a single inventory item by ID from DynamoDB."""

import json
import boto3
from typing import Any, Dict
from botocore.exceptions import ClientError

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps("Missing 'id' path parameter.")}

    item_id = event["pathParameters"]["id"]
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        response = table.get_item(Key={"item_id": item_id})
        item = response.get("Item")
        if not item:
            return {"statusCode": 404, "body": json.dumps("Item not found.")}
        return {"statusCode": 200, "body": json.dumps(item, default=str)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
