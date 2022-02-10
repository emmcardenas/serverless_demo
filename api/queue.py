import boto3
import json

SQS_URL = 'https://sqs.us-east-1.amazonaws.com/476168538798/serverless_queue_dev'

def receive_message_sqs():
    client_sqs = boto3.client('sqs', region_name='us-east-1')

    message = {}
    try:
        response = client_sqs.receive_message(
            QueueUrl = SQS_URL
        )
        messages = response['Messages']
    except KeyError:
        print('No messages on the queue!')
    
    for msg in messages:
        body = json.loads(msg['Body'])
        print(body)
    return body