from django.db import models
# Create your models here.

class Course(models.Model):
	courseID = models.CharField(primary_key=True, max_length=100, blank=False, default='')
	courseTitle = models.CharField(max_length=100, blank=True, default='')
	roomNum = models.CharField(max_length=100, blank=True, default='')

	class Meta:
		ordering = ('courseID', )


class Enrollment(models.Model):

	courseID = models.CharField(max_length=100, blank=False)
	studentID =  models.CharField(max_length=100, blank=False)
	
	class Meta:
		ordering = ('courseID', 'studentID')
		unique_together=(('courseID','studentID'),)



