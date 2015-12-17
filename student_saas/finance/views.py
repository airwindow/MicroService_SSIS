from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt
from finance.models import Tenant, Student, TenantAttribute, TenantAttributeValue


# the input must be serizable
class JsonResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JsonResponse, self).__init__(content, **kwargs)



@csrf_exempt
def tenant_attribute_list(request, tid):
	'''
	retrieve all added attrubutes belong to the tenant and add a new attribute to a tenant
	'''
	attributes = TenantAttribute.objects.filter(tenant_id = tid)
	if request.method == 'GET':
		print attributes
		response = [] 
		for attribute in attributes:
			item = {};
			item['tenant_id'] = attribute.tenant.tenant_id
			item['attribute_name'] = attribute.attribute_name
			item['attribute_type'] = attribute.attribute_type
			response.append(item)
		return JsonResponse(response)   

	# add a new attrbute for a tenant
	if request.method == 'POST':
		data = JSONParser().parse(request)
		# note the order of attribute in the table
		attribute = TenantAttribute(tenant_id = data['tenant_id'], attribute_name = data['attribute_name'], attribute_type = data['attribute_type'])
		attribute.save()
		return JsonResponse(data)



@csrf_exempt
def tenant_attribute(request, tid, attr_name):
	'''
	the RUD functions for tenant to manage its additional attributes
	'''
	# add does not exist exception checking! 
	attribute = TenantAttribute.objects.get(tenant_id = tid, attribute_name = attr_name)

	if request.method == 'DELETE':
		attribute.delete()
		return HttpResponse(status=200)

	if request.method == 'PUT':
		data = JSONParser().parse(request)
		attribute.attribute_name = data['attribute_name']
		attribute.attribute_type = data['attribute_type']
		attribute.save()
		return HttpResponse(status=200)



@csrf_exempt
def student_finance_list(request, tid):
	'''
	List all students of a tenant and add a student into a tenant's database
	'''
	if request.method == 'GET':
		students = Student.objects.filter(tenant_id = tid)
		response = []
		for student in students:
			item = {}
			item["tenant_id"] = student.tenant_id
			item["ssn"] = student.ssn
			item["first_name"] = student.first_name
			item["last_name"] = student.last_name
			item["balance"] = student.balance
			response.append(item)
		return JsonResponse(response)


	if request.method == 'POST':
		data = JSONParser().parse(request)
		attributes = TenantAttribute.objects.filter(tenant_id=data['tenant_id'])
		# insert common information for the student
		student = Student(ssn=data['ssn'], tenant_id=data['tenant_id'], first_name=data['first_name'], last_name=data['last_name'], balance=data['balance'])
		student.save()
		# insert extra information of the student(specified by the tenant)
		print data
		print attributes
		for attribute in attributes:
			print attribute.attribute_name
			if attribute.attribute_name in data:
				attribute_value = TenantAttributeValue(student_id=data['ssn'], tenant_id=data['tenant_id'], tenant_attribute_id=attribute.id, attribute_value=data[attribute.attribute_name])
				attribute_value.save()
		return JsonResponse(data)



@csrf_exempt
def student_finance(request, tid, ssn):
	'''
	Cause the model of Django. 
	"student_id" in TenantAttributeValue table refers to "ssn"(primary_key) in Student table
	'''

	'''
	List a student's finance info
	'''
	if request.method == 'GET':
		response = {};
		student = Student.objects.get(tenant_id = tid, ssn = ssn)
		response['ssn'] = student.ssn
		response['tenant_id'] = student.tenant_id
		response['first_name'] = student.first_name
		response['last_name'] = student.last_name
		response['balance'] = student.balance
		# the student's extra attributes(infromation)
		value_list = TenantAttributeValue.objects.filter(student_id = ssn, tenant_id=tid)
		for value_item in value_list:
			# retrieve the name of the attribute through the ID is attribute value item
			attribute = TenantAttribute.objects.get(id = value_item.tenant_attribute_id)
			response[attribute.attribute_name] = value_item.attribute_value
		return JsonResponse(response)


	'''
	Delete a student's finance info
	'''
	if request.method == 'DELETE':
		student = Student.objects.get(tenant_id = tid, ssn = ssn)
		student.delete()
		return HttpResponse(status=200)


	'''
	Update a student's finance info
	'''
	if request.method == 'PUT':
		# delete the student's record first
		student = Student.objects.get(tenant_id = tid, ssn = ssn)
		student.delete()

		# insert the student's new record into the database
		data = JSONParser().parse(request)
		attributes = TenantAttribute.objects.filter(tenant_id=data['tenant_id'])
		# insert common information for the student
		student = Student(ssn=data['ssn'], tenant_id=data['tenant_id'], first_name=data['first_name'], last_name=data['last_name'], balance=data['balance'])
		student.save()
		# insert extra information of the student(specified by the tenant)
		print data
		print attributes
		for attribute in attributes:
			print attribute.attribute_name
			if attribute.attribute_name in data:
				attribute_value = TenantAttributeValue(student_id=data['ssn'], tenant_id=data['tenant_id'], tenant_attribute_id=attribute.id, attribute_value=data[attribute.attribute_name])
				attribute_value.save()
		return JsonResponse(data)



@csrf_exempt
def tenant_list(request):
	'''
	List all tenants in the database and add a tenant into database
	'''
	if request.method == 'GET':
		tenants = Tenant.objects.all()
		response = []
		for tenant in tenants:
			item = {}
			item['tenant_id'] = tenant.tenant_id
			item['university'] = tenant.university
			item['state'] = tenant.state
			response.append(item)
		return JsonResponse(response)

	if request.method == 'POST':
		try:
			data = JSONParser().parse(request)
			t = Tenant(tenant_id = data['tenant_id'], university = data['university'], state = data['state'])
			t.save()
			return JsonResponse(data)
		except Tenant.DoesNotExist:
			return HttpResponse(status=500)


	
@csrf_exempt
def tenant_detail(request, tid):
	'''
	RUD over tenant information
	'''
	#GET/DELETE/UPDATE
	try:
		tenant = Tenant.objects.get(pk=tid)
	except:
		return HttpResponse(status=404)

	response = {};
	response['tenant_id'] = tenant.tenant_id
	response['university'] = tenant.university
	response['state'] = tenant.state

	if request.method == 'GET':
		return JsonResponse(response)
	elif request.method == 'DELETE':
		tenant.delete()
		return JsonResponse(response)
	elif request.method ==  'PUT':
		try:
			data = JSONParser().parse(request)
			tenant.university = data['university']
			tenant.state = data['state']
			tenant.save()
			return JsonResponse(data)
		except Tenant.DoesNotExist:
			return HttpResponse(status=500)