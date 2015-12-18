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



def get_k12_test_queue():
    '''
    a queue of testing 'K12Info'
    '''
    q = Queue.Queue()
    # List all students in K12
    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    # Add a new student into K12
    body = {'SSN':'111199999', 'FirstName':'Lin', 'LastName':'Lucy', 'Shoes':'Nike', 'IQ':'195'}; 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'POST', body))
    # List all students in K12
    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    # Retrieve a student's information in K12
    body = {'SSN':'111199999'} 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    # Delete a student in K12
    body = {'SSN':'111199999'} 
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'DELETE', body))
    # List all students in K12
    body = {}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    # Retrieve a student's informaiton in K12
    body = {'SSN':'111199999'}
    q.put(wrap_request('K12Info', 'ClientOneQueue', id_generator(), 'GET', body))
    return q



def get_tenant_test_queue():
    '''
    a queue of testing 'FinanceTenantInfo'
    '''
    q = Queue.Queue()
    # List all tenants
    body = {}
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Add a new tenant
    body = {"tenant_id":"111111111","university":"Columbia","state":"NY"}; 
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # Add a new tenant
    body = {"tenant_id":"111111112","university":"Yale","state":"CT"}
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # List all tenants
    body = {}
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Retrieve a tenant
    body = {"tenant_id":"111111111"} 
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Update a tenant
    body = {"tenant_id":"111111112","university":"MIT","state":"MA"} 
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'PUT', body))
    # Retrieve a tenant
    body = {"tenant_id":"111111112"}
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Delete a tenant
    body = {"tenant_id":"111111112"} 
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'DELETE', body))
    # List all tenants
    body = {}
    q.put(wrap_request('FinanceTenantInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    return q



def get_attribute_test_queue():
    '''
    a queue of testing 'FinanceTenantAttributeInfo'
    '''
    q = Queue.Queue()
    # List all additional attributes customermized by a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Add a new attribute for a tenant
    body = {"tenant_id": "111111111", "attribute_name": "grade", "attribute_type": "String"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # List all additional attributes added by a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Update a attribute's name 
    body = {"tenant_id": "111111111", "old_attribute_name": "grade", "attribute_name": "GPA", "attribute_type": "String"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'PUT', body))
    # List all additional attributes added by a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Delete a attribute of a tenant
    body = {"tenant_id": "111111111", "old_attribute_name": "GPA"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'DELETE', body))
    # List all additional attributes added by a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Add a new attribute for a tenant
    body = {"tenant_id": "111111111", "attribute_name": "GPA", "attribute_type": "String"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # Add a new attribute for a tenant
    body = {"tenant_id": "111111111", "attribute_name": "major", "attribute_type": "String"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # List all attributes added by a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    return q



def get_student_test_queue():
    '''
    a queue of testing 'FinanceStudentInfo' 
    note: only operation on student not attribute_
    '''
    q = Queue.Queue()
    # List all  students of a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Add a student of a tenant
    body = {"first_name":"Tom","last_name":"Cat","tenant_id":"111111111","major":"CE","GPA":"4.3","ssn":"123456789","balance":"0.0"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'POST', body))
    # List all  students of a tenant
    body = {"tenant_id": "111111111"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Update a student's information
    body = {"tenant_id": "111111111", "ssn": "123456789", "first_name": "Tom", "last_name" : "Cat", "balance" : "0.0", "major" : "CS", "GPA" : "4.33"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'PUT', body))
    # List a student's information
    body = {"tenant_id": "111111111", "ssn": "123456789"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'GET', body))
    # Delete a attribute from a tenant
    body = {"tenant_id": "111111111", "old_attribute_name": "GPA"}
    q.put(wrap_request('FinanceTenantAttributeInfo', 'ClientOneQueue', id_generator(), 'DELETE', body))
    # List a student's information
    body = {"tenant_id": "111111111", "ssn": "123456789"}
    q.put(wrap_request('FinanceStudentInfo', 'ClientOneQueue', id_generator(), 'GET', body))
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
    # test_queue = get_tenant_test_queue()
    # test_queue = get_attribute_test_queue()
    test_queue = get_student_test_queue()

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