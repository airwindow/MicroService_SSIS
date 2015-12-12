import boto3
import json
import time



# send message to APIGateWayQueue
def send_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'Get'
    message['ResponseQueue'] = 'ClientOneQueue'
    body = {};
    body['SSN'] = '111111111'
    message['Body'] = body
    # print json.dumps(message)
    response = gateway_queue.send_message(MessageBody = json.dumps(message))



# read message from my queue
def get_message():
    for message in client_queue.receive_messages():
        print message.body



# main function
# step 1: load url table
# step 2: perdiocally read message from input queue and proxy the request
if __name__ == '__main__':
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    gateway_queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')
    client_queue = sqs.get_queue_by_name(QueueName='ClientOneQueue')
    timeout = time.time() + 5  # 1 seconds from now
    while True:
        if time.time() > timeout:
            send_message()
            get_message()
            