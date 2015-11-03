from celery import shared_task

from ssis.celery import app

@shared_task(queue='default, response, result, students, courses')
def route(request):
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
    return app.send_task('students.tasks.process_student', args=args, kwargs=kwargs, queue='students', routing_key='students.request')
