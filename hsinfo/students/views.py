from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import students.get_item as db_get
import students.add_item as db_add
import students.update_item as db_update
import students.delete_item as db_delete

class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)

# Create your views here.

@csrf_exempt
def student_list(request):
    if request.method == 'GET':
        result = db_get.get_all()
        return JsonResponse(result['Items'])
    if request.method == 'POST':
        data = JSONParser().parse(request)
        db_add.load_from_json_dict(data)
        return JsonResponse(data)

@csrf_exempt
def student_detail(request, ssn):
    if request.method == 'GET':
        student = {'SSN': ssn}
        result = db_get.get(student)
        return JsonResponse(result['Item'])
    if request.method == 'PUT':
        student = {'SSN': ssn}
        data = JSONParser().parse(request)
        result = db_update.update(student, data)
        return JsonResponse(data)
    if request.method == 'DELETE':
        student = {'SSN': ssn}
        result = db_delete.delete(student)
        return HttpResponse()
