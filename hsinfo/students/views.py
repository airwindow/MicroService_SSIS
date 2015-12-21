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
        students = dbop.get_all()
        reponse = []
        return JsonResponse(students["Items"])

    # add a new student into K-12 Database
    if request.method == 'POST':
        data = JSONParser().parse(request)
        student = {'SSN': data['SSN']}
        result = dbop.get(student)
        if 'Item' in result:
            return HttpResponse("The student exists!", status=400)
        dbop.add(data)
        return HttpResponse(status = 200)



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
            return HttpResponse(status=404)
        return JsonResponse(result['Item'])
    
    # Modify an existing student
    if request.method == 'PUT':
        student = {'SSN': ssn}
        data = JSONParser().parse(request)
        result = dbop.get(student)
        if 'Item' not in result:
            return HttpResponse("The student does not exist!", status=404)
        dbop.delete(student)
        dbop.add(data)
        return HttpResponse(status = 200)
    
    # Delete a student 
    if request.method == 'DELETE':
        student = {'SSN': ssn}
        result = dbop.get(student)
        if 'Item' not in result:
            return HttpResponse("The student does not exist!", status=404)
        result = dbop.delete(student)
        return HttpResponse()
