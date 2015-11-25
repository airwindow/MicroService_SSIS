from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from courses.models import Course,Enrollment
from students.models import Student
from students.models import Enrollment as SEnrollment
from courses.serializers import CourseSerializer,EnrollSerializer
from students.serializers import EnrollSerializer as SEnrollSerializer

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
			serializer.save()
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
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		delete_enroll(cID=cID)
		print "test"
		course.delete(using='course')
		return HttpResponse(status=204)



@csrf_exempt
def enroll_list(request):

	if request.method == 'GET':
		enroll = Enrollment.objects.using('course').all()
		serializer = EnrollSerializer(enroll, many=True)
		return JSONResponse(serializer.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		try:
			CouObj = Course.objects.using("course").get(courseID=data["courseID"])
		except Course.DoesNotExist:
			return HttpResponse(status=404)
		try:
			if data["studentID"]<"n":
				StuObj = Student.objects.using("student1").get(studentID=data["studentID"])
			else:
				StuObj = Student.objects.using("student2").get(studentID=data["studentID"])
		except Student.DoesNotExist:
			return HttpResponse(status=404)
		serializer_cou = EnrollSerializer(data=data)
		serializer_stu = SEnrollSerializer(data=data)
		if serializer_stu.is_valid() and serializer_cou.is_valid():
			serializer_stu.save()
			serializer_cou.save()
			return JSONResponse(serializer_cou.data, status=201)
		return JSONResponse(serializer_cou.errors, status=400)


@csrf_exempt
def enroll_course_detail(request, cID):
	try:
		enroll = Enrollment.objects.using('course').get(courseID=cID)
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'DELETE':
		delete_enroll(cID=cID)
		return HttpResponse(status=204)

@csrf_exempt
def delete_enroll(cID):
	print "test"
	enroll_stu1 = None
	try:
		enroll_stu1 = SEnrollment.objects.using('student1').filter(courseID=cID) 
	except SEnrollment.DoesNotExist:
		pass
	enroll_stu2 = None
	try:
		enroll_stu2 = SEnrollment.objects.using('student2').filter(courseID=cID)
	except SEnrollment.DoesNotExist:
		pass
	enroll_cou = None;
	try:
		enroll_cou = Enrollment.objects.using('course').filter(courseID=cID)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)
	if enroll_stu1:
		enroll_stu1.delete()
	if enroll_stu2:
		enroll_stu2.delete()
	if enroll_cou:
		enroll_cou.delete()
	return HttpResponse(status=204)

@csrf_exempt
def enroll_detail(request, sID, cID):

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
		try:
			if sID[0]<"n":
				enroll_stu = SEnrollment.objects.using("student1").filter(studentID=sID).filter(courseID=cID)
			else:
				enroll_stu = SEnrollment.objects.using("student2").filter(studentID=sID).filter(courseID=cID)
		except SEnrollment.DoesNotExist:
			return HttpResponse(status=404)
		serializer = EnrollSerializer(enroll, data=data)
		serializer_stu = SEnrollSerializer(enroll_stu,data=data)
		if serializer.is_valid() and serializer_stu.is_valid():
			serializer.save()
			serializer_stu.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':
		enroll.delete()
		if sID[0]<"n":
			enroll_stu = SEnrollment.objects.using("student1").filter(studentID=sID).filter(courseID=cID)
			enroll_stu.delete()
		else:
			enroll_stu = SEnrollment.objects.using("student2").filter(studentID=sID).filter(courseID=cID)
			enroll_stu.delete()
		return HttpResponse(status=204)