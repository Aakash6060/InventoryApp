import json
import boto3

def lambda_handler(event, context):
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter.")
        }

    location_id = int(event['pathParameters']['id'])
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    try:
        response = table.query(
            IndexName='LocationIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key('location_id').eq(location_id)
        )
        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }