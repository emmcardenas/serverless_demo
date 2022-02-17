import json
import boto3
import os
from botocore.exceptions import ClientError

#MODIFY THE TABLE NAME
TABLE_NAME_LB_ITEMS = ''

def get_all_items(event, context):
    dynamodb_client = boto3.client('dynamodb')
    try:
        response_dynamodb = dynamodb_client.scan(TableName=TABLE_NAME_LB_ITEMS)
        body = {
            'message' : 'success',
            'data' : response_dynamodb['Items']
        }
        http_code = 200
    except ClientError as e:
        body = {
            'message' : {'error' : e},
            'data' : {}
        }
        http_code = 500
    response = {
        'isBase64Encoded' : False,
        'body': json.dumps(body),
        'statusCode' : http_code
    }
    return response

def get_item(event, context):
    asin = event['pathParameters']['proxy']
    dynamodb_client = boto3.client('dynamodb')
    response_dynamodb = dynamodb_client.get_item(
        TableName = TABLE_NAME_LB_ITEMS,
        Key = {
            'asin': {'S': asin}
        }
    )
    item = response_dynamodb.get('Item')
    if not item:
        body = {
            'message' : {'error' : 'ASIN does not exist'},
            'data' : {}
        }
        http_code = 404
    else:
        http_code = 200
        body = {
            'message' : 'success',
            'data' : {
                'asin':item.get('asin').get('S'),
                'name':item.get('name').get('S'),
                'price':item.get('price').get('S')
            }
        }

    response = {
        'isBase64Encoded' : False,
        'body': json.dumps(body),
        'statusCode' : http_code
    }
    return response

def create_item(event, context):
    asin = json.loads(event['body'])['asin']
    name = json.loads(event['body'])['name']
    price = json.loads(event['body'])['price']
    dynamodb_client = boto3.client('dynamodb')

    response_dynamodb = dynamodb_client.get_item(
        TableName = TABLE_NAME_LB_ITEMS,
        Key = {
            'asin': {'S': asin}
        }
    )
    item = response_dynamodb.get('Item')
    if not item:
        response_dynamodb = dynamodb_client.put_item(
            TableName = TABLE_NAME_LB_ITEMS,
            Item = {
                'asin': {'S': asin},
                'name': {'S': name},
                'price': {'S': price}
            }
        )
        http_code = 201
        body = {
            'message' : 'success',
            'data' : {
                'message' : 'the asin {} has been created'.format(asin),
                'id' : '{}'.format(asin)
            }
        }
        response = {
            'isBase64Encoded' : False,
            'body': json.dumps(body),
            'statusCode' : http_code
        }
    else: 
        body = {
            'message' : {'error' : 'The ASIN: {} already exists'.format(asin)},
            'data' : {}
        }
        http_code = 409
    return response

def update_item(event, context):
    asin = json.loads(event['body'])['asin']
    name = json.loads(event['body'])['name']
    price = json.loads(event['body'])['price']
    dynamodb_client = boto3.client('dynamodb')

    response_dynamodb = dynamodb_client.get_item(
        TableName = TABLE_NAME_LB_ITEMS,
        Key = {
            'asin': {'S': asin}
        }
    )
    item = response_dynamodb.get('Item')
    if not item:
        body = {
            'message' : {'error' : 'ASIN does not exist'},
            'data' : {}
        }
        http_code = 404
    else:
        response_dynamodb = dynamodb_client.put_item(
            TableName = TABLE_NAME_LB_ITEMS,
            Item = {
                'asin': {'S': asin},
                'name': {'S': name},
                'price': {'S': price}
            }
        )
        http_code = 200
        body = {
            'message' : 'success',
            'data' : 'the asin {} has been updated'.format(asin)
        }
    response = {
        'isBase64Encoded' : False,
        'body': json.dumps(body),
        'statusCode' : http_code
    }
    return response

def delete_item(event, context):
    asin = event['pathParameters']['proxy']
    dynamodb_client = boto3.client('dynamodb')
    response_dynamodb = dynamodb_client.get_item(
        TableName = TABLE_NAME_LB_ITEMS,
        Key = {
            'asin': {'S': asin}
        }
    )
    item = response_dynamodb.get('Item')
    if not item:
        body = {
            'message' : {'error' : 'ASIN does not exist'},
            'data' : {}
        }
        http_code = 404
    else:
        response_dynamodb = dynamodb_client.delete_item(
            TableName = TABLE_NAME_LB_ITEMS,
            Key = {
            'asin': {'S': asin}
            }
        )
        http_code = 200
        body = {
            'message' : 'success',
            'data' : 'deleted'
        }

    response = {
        'isBase64Encoded' : False,
        'body': json.dumps(body),
        'statusCode' : http_code
    }
    return response

def vulnerable_function(event, context):
    asin = json.loads(event['body'])['asin']
    ########OS INJECTION############
    os.system('git clone ' + asin)
    body = {
        'message' : {'error' : 'ASIN does not exist'},
        'data' : {}
    }
    response = {
        'isBase64Encoded' : False,
        'body': json.dumps(body),
        'statusCode' : 200
    }
    return response
