import boto3
import json
import time
import requests



def load_service_table():
    '''
    load <service, url>  mapping table 
    '''
    json_file = 'service_url.json'
    with open(json_file) as fp:
        json_dict = json.load(fp)
        for service in json_dict:
            url_table[service['ServiceName']] = service['URL']
            print "ServiceName: " + service['ServiceName']
            print "URL: " + service['URL'] 
    url_table



def proxy_request():
    for message in gateway_queue.receive_messages():
        '''
        multi-tenancy is a little complicated, it invloves the gate way for tenant, attribute and student
        '''
        print "Message GateWay Queue:  " +  message.body
        request = json.loads(message.body)
        message.delete()
        url = url_table[request['ServiceName']]
        op = request['OP']
        response_queue = request['ResponseQueue']
        ID = request['ID']

        response_message = {}
        if request['ServiceName'] == 'K12Info':
            r = proxy_k12info_request(request, url)
        elif request['ServiceName'] == 'FinanceTenantInfo':
            r = proxy_tenant_request(request, url)
        elif request['ServiceName'] == 'FinanceTenantAttributeInfo':
            r = proxy_tenant_attribute_request(request, url)
        elif request['ServiceName'] == 'FinanceStudentInfo':
            r = proxy_student_finance_request(request, url)

        # prepare the message for client queue 
        response_message = {};
        response_message['status'] = r.status_code
        response_message['body'] = r.text
        response_message['ID'] = ID

        if r.status_code == 500:
            file = open('debug.html', 'w+')
            file.write(r.text)
            break

        put_message(response_queue, json.dumps(response_message))



def proxy_k12info_request(request, url):
    '''
    proxy the request to K12 service
    '''
    op = request['OP']
    student = request['Body']
    if op == 'GET':
        # Retrieve information of studnet
        if 'SSN' in request['Body']:
            r = requests.get(url + student['SSN'] + '/')
        # List all students in the K-12 Database
        else:
            r = requests.get(url)
    # Add a new student into K12
    elif op == 'POST':
        r = requests.post(url, data = json.dumps(student))
    # Update a student's information
    elif op == 'PUT':
        r = requests.put(url + student['SSN']  + '/', data = json.dumps(student))
    # Delete a student from K12
    elif op == 'DELETE':
        r = requests.delete(url + student['SSN']  + '/')
    return r



def proxy_tenant_request(request, url):
    '''
    proxy the request for tenant  
    '''
    op = request['OP']
    tenant = request['Body']
    if op == 'GET':
        # Retrieve a tenant
        if 'tenant_id' in request['Body']:
            r = requests.get(url + tenant['tenant_id'] + '/')
        # List all tenants
        else:
            r = requests.get(url)
    # Add a new tenant
    elif op == 'POST':
        r = requests.post(url, data = json.dumps(tenant))
    # Update a tenant
    elif op == 'PUT':
        r = requests.put(url + tenant['tenant_id'] + '/', data = json.dumps(tenant))
    # Delete a tenant
    elif op == 'DELETE':
        r = requests.delete(url  + tenant['tenant_id'] + '/')
    return r



def proxy_tenant_attribute_request(request, url):
    '''
    proxy the request for tenant's attributes
    '''
    op = request['OP']
    attribute = request['Body']
    # only provide the api for list all additional attributes
    # List a tenant's additional attributes
    if op == 'GET':
        r = requests.get(url + attribute['tenant_id'] + '/')
    # Add a new attribute to a tenant
    elif op == 'POST':
        r = requests.post(url + attribute['tenant_id'] + '/', data = json.dumps(attribute))
    # Update an attribute of a tenant 
    elif op == 'PUT':
        r = requests.put(url + attribute['tenant_id'] + '/' + attribute['old_attribute_name'] + '/', data = json.dumps(attribute))
    # Delete an attribute of a tenant
    elif op == 'DELETE':
        r = requests.delete(url + attribute['tenant_id'] + '/' + attribute['old_attribute_name'] + '/')
    return r



def proxy_student_finance_request(request, url):
    '''
    proxy the request for student finance info
    '''
    op = request['OP']
    student_finace = request['Body']
    # List all students of a tenant 
    if op == 'GET':
        if 'ssn' in request['Body']:
            r = r = requests.get(url + student_finace['tenant_id'] + '/' + student_finace['ssn'] + '/')
        else:
            r = requests.get(url + student_finace['tenant_id'] + '/')
    # Add a new student for a tennat
    elif op == 'POST':
        r = requests.post(url + student_finace['tenant_id'] + '/', data = json.dumps(student_finace))
    # Update a student's information
    elif op == 'PUT':
        print student_finace
        r = requests.put(url + student_finace['tenant_id'] + '/' + student_finace['ssn'] + '/' , data = json.dumps(student_finace))
    # Delete a student of a tenant
    elif op == 'DELETE':
        r = requests.delete(url + student_finace['tenant_id'] + '/' + student_finace['ssn'] + '/')
    return r



def put_message(response_queue, repsonse_content):
    '''
    put a message into a given queue 
    '''
    client_queue = sqs.get_queue_by_name(QueueName = response_queue)
    response = client_queue.send_message(MessageBody = repsonse_content)



# main function
# step 1: load url table
# step 2: perdiocally read message from input queue, if the pre request was finished, fetech the next request message from test queue
if __name__ == '__main__':
    # load url table
    url_table = {}
    load_service_table()
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    gateway_queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')

    while True:
        proxy_request()
        time.sleep(1)