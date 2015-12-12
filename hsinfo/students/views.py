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



# Create your views here.
@csrf_exempt
def student_list(request):
    if request.method == 'GET':
        result = dbop.get_all()
        if 'Items' not in result:
            return HttpResponse(status=204)
        return JsonResponse(result['Items'])
    if request.method == 'POST':
        print request
        data = JSONParser().parse(request)
        print data
        dbop.load_from_json_dict(data)
        dbop.add(data)
        return JsonResponse(data)



@csrf_exempt
def student_detail(request, ssn):
    if request.method == 'GET':
        student = {'SSN': ssn}
        result = dbop.get(student)
        if 'Item' not in result:
            return HttpResponse(status=204)
        return JsonResponse(result['Item'])
    if request.method == 'PUT':
        student = {'SSN': ssn}
        data = JSONParser().parse(request)
        dbop.delete(student)
        dbop.add(data)
        return JsonResponse(data)
    if request.method == 'DELETE':
        student = {'SSN': ssn}
        result = dbop.delete(student)
        return HttpResponse()
