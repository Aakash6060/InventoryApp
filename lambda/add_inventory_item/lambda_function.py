"""Lambda function to add an inventory item to DynamoDB."""

import json
import uuid
import boto3
from typing import Any, Dict
from botocore.exceptions import ClientError


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        data = json.loads(event["body"])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {"statusCode": 400, "body": json.dumps("Invalid request body.")}

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")
    item_id = str(uuid.uuid4())

    try:
        table.put_item(
            Item={
                "item_id": item_id,
                "item_name": data["item_name"],
                "item_description": data["item_description"],
                "item_qty": int(data["item_qty"]),
                "item_price": float(data["item_price"]),
                "location_id": int(data["location_id"]),
            }
        )
        return {"statusCode": 200, "body": json.dumps(f"Item {item_id} added.")}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
