"""Lambda function to retrieve all inventory items for a specific location ID."""

import json
import boto3
from boto3.dynamodb.conditions import Key
from typing import Any, Dict
from botocore.exceptions import ClientError

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {"statusCode": 400, "body": json.dumps("Missing 'id' path parameter.")}

    location_id = int(event["pathParameters"]["id"])
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        response = table.query(
            IndexName="LocationIndex",
            KeyConditionExpression=Key("location_id").eq(location_id),
        )
        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps(items, default=str)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
