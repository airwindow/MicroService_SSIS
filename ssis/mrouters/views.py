from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from mrouters.tasks import route

# Create your views here.
def route_request(request):
    '''
    print type(request)
    print request
    print dir(request)
    print request.method
    print request.get_full_path()
    print request.path
    print request.GET
    print request.POST
    args = [request.method, request.get_full_path()]
    kwargs = {}
    if request.method == 'GET':
        kwargs[request.method] = request.GET
    elif request.method == 'POST':
        kwargs[request.method] = request.POST
    result = app.send_task('students.tasks.process_student', args=args, kwargs=kwargs, queue='students', routing_key='students.request')
    '''
    result = route(request)
    print type(result)
    print dir(result)
    print result.task_id
    print result.backend
    print result.state
    print result.ready()
    ans = result.get(timeout=2)
    print ans
    print result.result
    return HttpResponse('test', status=400)
