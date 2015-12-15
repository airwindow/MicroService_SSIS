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
        print "Message at APIGateWayQueue:  " +  message.body
        request = json.loads(message.body)
        message.delete()
        # extract the information for proxying request
        url = url_table['ServiceName']
        op = request['OP']
        student = request['Body']
        response_queue = request['ResponseQueue']
        ID = request['ID']

        # extract the student's ssn 
        ssn = student['SSN']
        r = requests.get(url + ssn)

        # prepare the message for client queue 
        response_message = {};
        response_message['status'] = r.status_code
        response_message['body'] = r.text

        file = open('debug.html', 'w+')
        file.write(r.text)





        response_message['ID'] = ID
        put_message(response_queue, json.dumps(response_message))



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

    while True:
        proxy_request()
        time.sleep(5)