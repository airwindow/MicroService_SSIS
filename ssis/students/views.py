from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from students.models import Student
from students.models import Enrollment
from students.serializers import StudentSerializer
from students.serializers import EnrollSerializer
from courses.models import Course
from courses.models import Enrollment as CEnrollment
from courses.serializers import EnrollSerializer as CEnrollSerializer


# Import Libs for changing Schema 
from django.db import models
from django.db import connection, DatabaseError, IntegrityError
from django.db.models.fields import IntegerField, TextField, CharField, SlugField



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def student_list(request):
	"""
   	List all code students, or create a new students.
	"""
	if request.method == 'GET':
		s1 = Student.objects.using('student1').all()
		s2 = Student.objects.using('student2').all()
		#students = s1&s2
		serializer1 = StudentSerializer(s1, many=True)
		#print serializer1.data
		serializer2 = StudentSerializer(s2, many=True)
		#print serializer2.data
		return JSONResponse(serializer1.data+serializer2.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		print data
		serializer = StudentSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def student_detail(request, sID):
	"""
	Retrieve, update or delete a code snippet.
	"""
	try:
		if sID[0]<="m":
			student = Student.objects.using('student1').get(studentID=sID)
		else:
			student = Student.objects.using('student2').get(studentID=sID)
	except Student.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = StudentSerializer(student)
		return JSONResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = StudentSerializer(student, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)

	elif request.method == 'DELETE':
		enroll_delete(sID=sID)
		print "test"
		student.delete()
		return HttpResponse(status=204)



@csrf_exempt
def enroll_list(request):
	"""
   	List all enrollments, or create a new enrollment.
	"""
	if request.method == 'GET':
		enroll1 = Enrollment.objects.using("student1").all()
		enroll2 = Enrollment.objects.using("student2").all()
		serializer1 = EnrollSerializer(enroll1, many=True)
		serializer2 = EnrollSerializer(enroll2, many=True)
		#print serializer1.data
		return JSONResponse(serializer1.data+serializer2.data)
		
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		try:
			CouObj = Course.objects.using("course").get(courseID=data["courseID"])
		except Course.DoesNotExist:
			return HttpResponse(status=404)
		try:
			if data["studentID"][0]<"n" :
				StuObj = Student.objects.using("student1").get(studentID=data["studentID"])
			else:
				StuObj = Student.objects.using("student2").get(studentID=data["studentID"])
		except Student.DoesNotExist:
			return HttpResponse(status=404)
		serializer_stu = EnrollSerializer(data=data)
		serializer_cou = CEnrollSerializer(data=data)
		if serializer_stu.is_valid() and serializer_cou.is_valid():
			serializer_stu.save()
			serializer_cou.save()
			return JSONResponse(serializer_stu.data, status=201)

		return JSONResponse(serializer_stu.errors, status=400)



@csrf_exempt
def enroll_student_detail(request, sID):
	"""
	Retrieve, update or delete a enrollment.
	"""
	try:
		if sID[0]<="m":
			enroll = Enrollment.objects.using('student1').get(studentID=sID)
		else:
			enroll = Enrollment.objects.using('student2').get(studentID=sID)		
		serializer = EnrollSerializer(enroll)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll)
		return JSONResponse(serializer.data)

	elif request.method == 'DELETE':
		enroll_delete(sID=sID)
		return HttpResponse(status=204)

@csrf_exempt
def enroll_delete(sID):
	enroll = None
	enroll_cou = None
	try:
		if sID[0]<="m":
			enroll = Enrollment.objects.using('student1').filter(studentID=sID)
		else:
			enroll = Enrollment.objects.using('student2').filter(studentID=sID)
	except Enrollment.DoesNotExist:
		pass
	try:
		enroll_cou = CEnrollment.objects.using('course').filter(studentID=sID)
	except CEnrollment.DoesNotExist:
		pass
	if enroll:
		enroll.delete()
	if enroll_cou:
		enroll_cou.delete()

@csrf_exempt
def enroll_detail(request, sID, cID):
	"""
	Retrieve, update or delete a enrollment.
	"""
	try:
		if sID[0]<="m":
			enroll_stu = Enrollment.objects.using('student1').filter(studentID=sID).filter(courseID=cID)
		else:
			enroll_stu = Enrollment.objects.using('student2').filter(studentID=sID).filter(courseID=cID)
		enroll_cou = CEnrollment.objects.using('course').filter(studentID=sID).filter(courseID=cID)
		serializer_stu = EnrollSerializer(enroll_stu)
		serializer_cou = CEnrollSerializer(enroll_cou)
	except Enrollment.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = EnrollSerializer(enroll_stu)
		return JSONResponse(serializer_stu.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer_stu = EnrollSerializer(enroll_stu, data=data)
		serializer_cou = CEnrollSerializer(enroll_cou,data=data)
		if serializer_stu.is_valid() and serializer_cou.is_valid():
			serializer_stu.save()
			serializer_cou.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer_stu.errors, status=400)
	elif request.method == 'DELETE':
		enroll_stu.delete()
		enroll_cou.delete()
		return HttpResponse(status=204)




@csrf_exempt
def schema_operations(request):
	"""
	add column into the schema
	"""
	if request.method == 'POST':
		data = JSONParser().parse(request)
		field_name = data["field_name"]
		field_type = data["field_type"]
		default_value = data["default_value"]
		if field_type == "IntegerField" :
			field = models.IntegerField(default = default_value)
		elif field_type == "TextField" :
			field = models.TextField(default = default_value)
		elif field_type == "SlugField" :
			field = models.SlugField(default = default_value)
		else :
			field = models.CharField(max_length=50, default = default_value)
		field.set_attributes_from_name(field_name)
		try:
			with connection.schema_editor() as schema_editor:
				schema_editor.add_field(Student, field)
		except Student.DoesNotExist:
			return HttpResponse(status=404)
		return HttpResponse(status=200)