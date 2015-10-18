from django.db import models
# Create your models here.
class Student(models.Model):
	studentID = models.CharField(max_length=100, blank=True, default='');
	lastName = models.CharField(max_length=100, blank=True, default='');
	firstName = models.CharField(max_length=100, blank=True, default='');

	class Meta:
		ordering = ('studentID', )


