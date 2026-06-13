import json
import boto3
import uuid
from datetime import datetime, timezone

# Connect to DynamoDB and point to the watchlist table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('watchlist')

def lambda_handler(event, context):
    # This is the entry point AWS calls on every request
    # It checks the HTTP method and URL path to route to the right function
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'POST' and path == '/items':
        return add_item(event)
    elif http_method == 'GET' and path == '/items':
        return get_items()
    elif http_method == 'GET' and '/items/' in path:
        item_id = event['pathParameters']['id']
        return get_item(item_id)
    elif http_method == 'PATCH' and '/items/' in path:
        item_id = event['pathParameters']['id']
        return update_item(event, item_id)
    elif http_method == 'DELETE' and '/items/' in path:
        item_id = event['pathParameters']['id']
        return delete_item(item_id)
    else:
        return response(404, {'error': 'Not found'})

def add_item(event):
    # Parse the request body, generate a unique ID, and save the new item to DynamoDB
    body = json.loads(event['body'])
    item = {
        'item_id': str(uuid.uuid4()),
        'title': body['title'],
        'type': body['type'],
        'platform': body['platform'],
        'status': body.get('status', 'want to watch'),
        'added_at': datetime.now(timezone.utc).isoformat()
    }
    table.put_item(Item=item)
    return response(201, item)

def get_items():
    # Scan the entire DynamoDB table and return all items
    result = table.scan()
    return response(200, result['Items'])

def get_item(item_id):
    # Look up a single item by its ID, return 404 if it doesn't exist
    result = table.get_item(Key={'item_id': item_id})
    if 'Item' not in result:
        return response(404, {'error': 'Item not found'})
    return response(200, result['Item'])

def update_item(event, item_id):
    # Update just the status field of an existing item
    body = json.loads(event['body'])
    status = body['status']
    table.update_item(
        Key={'item_id': item_id},
        UpdateExpression='SET #s = :s',
        ExpressionAttributeNames={'#s': 'status'},  # 'status' is a reserved word in DynamoDB so we alias it
        ExpressionAttributeValues={':s': status}
    )
    return response(200, {'message': 'Updated'})

def delete_item(item_id):
    # Delete an item from DynamoDB by its ID
    table.delete_item(Key={'item_id': item_id})
    return response(200, {'message': 'Deleted'})

def response(status_code, body):
    # Helper that formats every response the way API Gateway expects it
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }