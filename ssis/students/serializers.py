from rest_framework import serializers
from students.models import Student
from students.models import Enrollment

class StudentSerializer(serializers.Serializer):

    # class Meta:
    #     model = Student
    #     fields = ('studentID', 'lastName', 'firstName')


    studentID = serializers.CharField(required=False, allow_blank=True, max_length=100)
    lastName = serializers.CharField(required=False, allow_blank=True, max_length=100)
    firstName = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Student` instance, given the validated data.
        """
        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Student` instance, given the validated data.
        """
        instance.studentID = validated_data.get('studentID', instance.studentID)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.firstName = validated_data.get('firstName', instance.firstName)

        instance.save()
        return instance

class EnrollSerializer(serializers.HyperlinkedModelSerializer):

    studentID = StudentSerializer('studentID')
    courseID  = serializers.CharField(required=True, allow_blank=False, max_length=100)

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