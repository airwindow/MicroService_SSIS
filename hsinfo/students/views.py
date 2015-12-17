from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from students.lib import dbop as dbop



class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)



@csrf_exempt
def student_list(request):
    '''
    List all students in K-12 and add a student into K-12
    '''
    # List all students in the K-12 Database
    if request.method == 'GET':
        result = dbop.get_all()
        if 'Items' not in result:
            return HttpResponse(status=204)
        return JsonResponse(result['Items'])

    if request.method == 'POST':
        print request
        data = JSONParser().parse(request)
        print data
        # dbop.load_from_json_dict(data)
        dbop.add(data)
        return JsonResponse(data)



@csrf_exempt
def student_detail(request, ssn):
    # Add a new student
    '''
    RUD for students in K-12 Database

    '''

    # Retrieve a specific student
    if request.method == 'GET':
        student = {'SSN': ssn}
        result = dbop.get(student)
        if 'Item' not in result:
            return HttpResponse(status=204)
        return JsonResponse(result['Item'])
    
    # Modify an existing student
    if request.method == 'PUT':
        student = {'SSN': ssn}
        data = JSONParser().parse(request)
        dbop.delete(student)
        dbop.add(data)
        return JsonResponse(data)
    
    # Delete a student 
    if request.method == 'DELETE':
        student = {'SSN': ssn}
        result = dbop.delete(student)
        return HttpResponse()
