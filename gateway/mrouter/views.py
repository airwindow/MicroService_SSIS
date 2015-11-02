from django.shortcuts import render
from django.http import HttpResponse

import pika

BROKER_URL = 'amqp://ssis:ssis@localhost:5672/ssisvhost'

result = []

# Create your views here.
def route(request):
    print request

    parameters = pika.URLParameters(BROKER_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(exchange='students', routing_key='students.test', body='test')
    channel.close()
    return HttpResponse('test', status=400)
