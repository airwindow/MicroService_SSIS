import boto3
import json
import time
import string 
import random
import Queue



def id_generator(size = 10, chars = string.ascii_uppercase + string.digits):
    '''
    id generator for message (when the client receive a response, it could map the repoonse with a request)
    '''
    return ''.join(random.choice(chars) for _ in range(size))



def send_message(message):
    '''
    send message to APIGateWayQueue
    Note: the content in the body is the content we want to microservice
    '''
    response = gateway_queue.send_message(MessageBody = json.dumps(message))



# read message from my queue
def get_message():
    '''
    read  message from client queue and return the message's id 
    '''
    for message in client_queue.receive_messages():
        print "Message at Client Queue:  " +  message.body
        id = json.loads(message.body)['ID']
        message.delete()
        return id
 


def wrap_request(service_name, response_queue, id, op, body):
    '''
    wrap the micro service request into a message to APIGateWay
    Note: body is a dictionary type at here
    '''
    message = {}
    message['ServiceName'] = service_name
    message['OP'] = op
    message['ResponseQueue'] = 'ClientOneQueue'  
    message['ID'] = id 
    message['Body'] = body
    return message



def get_test_queue():
    '''
    a queue of test case which would be called serially
    '''
    q = Queue.Queue()
    
    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    
    body = {'SSN':'111199999', 'FirstName':'Lin', 'LastName':'Lucy', 'Shoes':'Nike', 'IQ':'195'}; 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'POST', body))

    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))

    body = {'SSN':'111199999'} 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))

    body = {'SSN':'111199999'} 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'DELETE', body))

    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))

    body = {'SSN':'111199999'}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    return q



# main function
# step 1: load url table
# step 2: perdiocally read message from input queue and proxy the request
if __name__ == '__main__':
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    gateway_queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')
    client_queue = sqs.get_queue_by_name(QueueName='ClientOneQueue')
    # Get test queue(filled with test cases)
    test_queue = get_test_queue()

    message = test_queue.get()
    send_message(message)
    wait_request_id = message['ID']

    while True:
        time.sleep(5)
        finish_request_id = get_message()
        if finish_request_id == wait_request_id and not test_queue.empty():
            message = test_queue.get()
            wait_request_id = message['ID']
            send_message(message)