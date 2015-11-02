from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from courses.models import Course,Enrollment
#from students.models import Student
from courses.serializers import CourseSerializer,EnrollSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


"""
@csrf_exempt
def course_list(request):
	
   	#List all code courses, or create a new course.
	
	if request.method == 'GET':
		courses = Course.objects.using('course').all()
		serializer = CourseSerializer(courses, many=True)
		print serializer.data
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = CourseSerializer(data=data)
		if serializer.is_valid():
			serializer.save(using='course')
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def course_detail(request, cID):
	
	#Retrieve, update or delete a code snippet.
	
	try:
		course = Course.objects.using('course').get(courseID=cID)
	except Course.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = CourseSerializer(course)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = CourseSerializer(course, data=data)
		if serializer.is_valid():
			serializer.save(using='course')
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		course.delete(using='course')
		return HttpResponse(status=204)





@csrf_exempt
def enroll_list(request):

	if request.method == 'GET':
		enroll = Enrollment.objects.using('course').using('course').all()
		serializer = EnrollSerializer(enroll, many=True)
		print serializer.data
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = EnrollSerializer(data=data)
		if serializer.is_valid():
			serializer.save(using='course')
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def enroll_course_detail(request, cID):
	
	#Retrieve, update or delete a enrollment.
	
	try:
		enroll = Enrollment.objects.using('course').get(courseID=cID)
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'DELETE':
		enroll.delete(using='course')
		return HttpResponse(status=204)

@csrf_exempt
def enroll_detail(request, sIDx, cID):

	#Retrieve, update or delete a enrollment.
	
	try:
		enroll = Enrollment.objects.using('course').filter(studentID=sID).filter(courseID=cID)
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = EnrollSerializer(enroll, data=data)
		if serializer.is_valid():
			serializer.save(using='course')
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		enroll.delete(using='course')
		return HttpResponse(status=204)

"""
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





@csrf_exempt
def enroll_list(request):
	"""
   	List all enrollments, or create a new enrollment.
	"""
	if request.method == 'GET':
		enroll = Enrollment.objects.all()
		serializer = EnrollSerializer(enroll, many=True)
		print serializer.data
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = EnrollSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def enroll_course_detail(request, cID):
	"""
	Retrieve, update or delete a enrollment.
	"""
	try:
		enroll = Enrollment.objects.get(courseID=cID)
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'DELETE':
		enroll.delete()
		return HttpResponse(status=204)

@csrf_exempt
def enroll_detail(request, sID, cID):
	"""
	Retrieve, update or delete a enrollment.
	"""
	try:
		enroll = Enrollment.objects.filter(studentID=sID).filter(courseID=cID)
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = EnrollSerializer(enroll, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		enroll.delete()
		return HttpResponse(status=204)