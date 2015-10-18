from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from courses.models import Course
from courses.serializers import CourseSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def course_list(request):
	"""
   	List all code courses, or create a new course.
	"""
	if request.method == 'GET':
		courses = Course.objects.all()
		serializer = CourseSerializer(courses, many=True)
		print serializer.data
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CourseSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def course_detail(request, cID):
	"""
	Retrieve, update or delete a code snippet.
	"""
	try:
		course = Course.objects.get(courseID=cID)
	except Course.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CourseSerializer(course)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CourseSerializer(course, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		course.delete()
		return HttpResponse(status=204)


