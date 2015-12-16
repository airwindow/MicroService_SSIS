from django.db import models

# Create your models here.

# Tenant table for recording information of tenants
class Tenant(models.Model):
	tenant_id = models.CharField(primary_key=True, max_length=20)
	university = models.CharField(max_length=50)
	state = models.CharField(max_length=10)


# Common finance information of a student
class Student(models.Model):
	ssn = models.CharField(primary_key=True, max_length=20)
	tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	balance = models.CharField(max_length=30, default='0.0')


# Additional attributes specified by a tenant
class TenantAttribute(models.Model):
	tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
	attribute_name = models.CharField(max_length=30)
	attribute_type = models.CharField(max_length=30)


# The value of additional attribute for a student(based on which tenant the student belong to)
class TenantAttributeValue(models.Model):
	# Directly use Django's referential model. Mataining integrity becomes much easier
	# ssn = models.CharField(primary_key=True, max_length=20)
	student = models.ForeignKey('Student', on_delete=models.CASCADE)
	tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE)
	tenant_attribute = models.ForeignKey('TenantAttribute', on_delete=models.CASCADE)
	# To account for diferent types specified by tenant. A string type seems to be a good fit.  
	attribute_value = models.CharField(max_length=100)