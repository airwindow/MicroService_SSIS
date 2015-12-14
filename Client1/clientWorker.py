import boto3
import json
import time
import string 
import random



# id generator for message (when the client receive a response, it could map the repoonse with a request)
def id_generator(size = 10, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# simulate POST Request message
def get_post_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'POST'
    message['ResponseQueue'] = 'ClientOneQueue'
    # the ID of the request  
    message['ID'] = id_generator()
    # the post request should have detail information
    body = {};
    # body['SSN'] = id_generator(10, '0123456789')
    body['SSN'] = '111111111'
    body['LastName'] = 'Mike'
    body['FirstName'] = 'Young'
    body['Shoes'] = 'Adidas'
    body['IQ'] = '180'
    message['Body'] = body
    return message



# simulate GET Request message
def get_get_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'GET'
    message['ResponseQueue'] = 'ClientOneQueue'
    # the ID of the request  
    message['ID'] = id_generator()
    body = {};
    # get test, ssn must be exist
    body['SSN'] = '111111111'
    message['Body'] = body
    return message



# simulate PUT Request message
def get_put_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'PUT'
    message['ResponseQueue'] = 'ClientOneQueue'
    # the ID of the request  
    message['ID'] = id_generator()
    body = {};
    # get test, ssn must be exist
    body['SSN'] = "111111111"
    body['LastName'] = 'Mike'
    body['FirstName'] = 'Young'
    body['Shoes'] = 'ACIS'
    body['IQ'] = '180'
    message['Body'] = body
    return message



# simulate DELETE Request message
def get_delete_message():
    message = {};
    message['ServcieName'] = 'K12Info'
    message['OP'] = 'DELETE'
    message['ResponseQueue'] = 'ClientOneQueue'
    # the ID of the request  
    message['ID'] = id_generator()

    body = {};
    # get test, ssn must be exist
    body['SSN'] = "111111111"
    message['Body'] = body
    return message



# Note the content in the body is the content we want to microservice
# send message to APIGateWayQueue
def send_message():
    message = get_get_message()
    response = gateway_queue.send_message(MessageBody = json.dumps(message))



# read message from my queue
def get_message():
    for message in client_queue.receive_messages():
        print "Message at Client Queue:  " +  message.body
        message.delete()



# main function
# step 1: load url table
# step 2: perdiocally read message from input queue and proxy the request
if __name__ == '__main__':
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    gateway_queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')
    client_queue = sqs.get_queue_by_name(QueueName='ClientOneQueue')
    send_message()
    while True:
        get_message()
        time.sleep(5)