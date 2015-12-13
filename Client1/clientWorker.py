import boto3
import json
import time
import string 
import random



# id generator for message (when the client receive a response, it could map the repoonse with a request)
def id_generator(size = 10, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 



# send message to APIGateWayQueue
def send_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'GET'
    message['ResponseQueue'] = 'ClientOneQueue'
    message['ID'] = id_generator()

    body = {};
    body['SSN'] = id_generator(10, '0123456789')
    message['Body'] = body
    print json.dumps(message)
    response = gateway_queue.send_message(MessageBody = json.dumps(message))



# read message from my queue
def get_message():
    for message in client_queue.receive_messages():
        print message.body
        message.delete



# main function
# step 1: load url table
# step 2: perdiocally read message from input queue and proxy the request
if __name__ == '__main__':
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    gateway_queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')
    client_queue = sqs.get_queue_by_name(QueueName='ClientOneQueue')
    timeout = time.time() + 2 # 2 seconds from now
    while True:
        if time.time() > timeout:
            # send_message()
            get_message()
            