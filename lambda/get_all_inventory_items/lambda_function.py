"""Lambda function to retrieve all inventory items from DynamoDB."""

import json
import boto3
from typing import Any, Dict
from botocore.exceptions import ClientError

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Inventory")

    try:
        response = table.scan()
        items = response.get("Items", [])
        return {"statusCode": 200, "body": json.dumps(items, default=str)}
    except ClientError as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
