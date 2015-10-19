from rest_framework import serializers
from courses.models import Course
from courses.models import Enrollment
from students.models import Student
from students.serializers import StudentSerializer
class CourseSerializer(serializers.Serializer):

    # class Meta:
    #     model = Student
    #     fields = ('studentID', 'lastName', 'firstName')


    courseID = serializers.CharField(required=True, allow_blank=False, max_length=100)
    courseTitle = serializers.CharField(required=False, allow_blank=True, max_length=100)
    roomNum = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Course` instance, given the validated data.
        """
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Course` instance, given the validated data.
        """
        instance.courseID = validated_data.get('courseID', instance.courseID)
        instance.courseTitle = validated_data.get('courseTitle', instance.courseTitle)
        instance.roomNum = validated_data.get('roomNum', instance.roomNum)

        instance.save()
        return instance

class EnrollSerializer(serializers.HyperlinkedModelSerializer):

    courseID = CourseSerializer('courseID')
    studentID = serializers.CharField(required=False, allow_blank=True, max_length=100)

    class Meta:
        model = Enrollment
        fields = ('courseID', 'studentID')

   
    def create(self, validated_data):
        """
        Create and return a new `Enrollment` instance, given the validated data.
        """
        return Enrollment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Enrollment` instance, given the validated data.
        """
        instance.courseID = validated_data.get('courseID', instance.courseID)
        instance.studentID = validated_data.get('studentID', instance.studentID)
       
        instance.save()
        return instance