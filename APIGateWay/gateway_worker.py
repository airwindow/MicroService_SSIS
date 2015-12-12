import boto3
import json
import time
import requests



# load service -> url mapping table 
def load_service_table():
    json_file = 'service_url.json'
    with open(json_file) as fp:
        json_dict = json.load(fp)
        for service in json_dict:
            url_table['ServiceName'] = service['URL']
            url_table['URL'] = service['URL']
    url_table



# query message from APIGateWayQueue
def proxy_request():
    for message in queue.receive_messages():
        print message.body
        request = json.loads(message.body)
        # extract the information for proxying request
        url = url_table['ServiceName']
        op = request['OP']
        student = request['Body']
        response_queue = request['ResponseQueue']

        ssn = student['SSN']
        r = requests.get(url + ssn)
        put_message(response_queue, r.text)
        print r.text



# put a message into a given queue 
def put_message(response_queue, repsonse_content):
    client_queue = sqs.get_queue_by_name(QueueName = response_queue)
    response = client_queue.send_message(MessageBody = repsonse_content)




# main function
# step 1: load url table
# step 2: perdiocally read message from input queue and proxy the request
if __name__ == '__main__':
    # load url table
    url_table = {}
    load_service_table()
    # Get the sqs service 
    sqs = boto3.resource('sqs')
    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='APIGateWayQueue')


    timeout = time.time() + 1  # 1 seconds from now
    while True:
        if time.time() > timeout:
            proxy_request()