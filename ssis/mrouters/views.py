from django.shortcuts import render
from django.http import HttpResponse

from ssis.celery import app

# Create your views here.
def route_request(request):
    print dir(app)
    print request
    print 'to route!'

    print dir(request)
    if request.method == 'GET':
        print 'GET!'
    result = app.send_task('app.task.process_student', [request.body], queue='students', routing_key='students.request')
    print dir(result)
    print result.backend
    print result
    return HttpResponse('test', status=400)
