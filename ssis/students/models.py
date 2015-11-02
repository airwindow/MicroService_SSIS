from django.db import models
#from django.utils import timezone
#import architect
# Create your models here.
#@architect.install('partition', type='range', subtype='date', constraint='day', column='timing')

class Student(models.Model):
	studentID = models.CharField(primary_key = True, max_length=100, blank=False, default='')
	lastName = models.CharField(max_length=100, blank=True, default='')
	firstName = models.CharField(max_length=100, blank=True, default='')
	#timing = models.DateTimeField(default=timezone.now)
	class Meta:
		ordering = ('studentID', )


class Enrollment(models.Model):

	studentID = models.ForeignKey('Student')
	courseID  = models.CharField(max_length=100, blank=False)
	
	class Meta:
		ordering = ('courseID', 'studentID')




