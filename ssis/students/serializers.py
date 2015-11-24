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
        #print validated_data["studentID"][0]>="n"
        if validated_data["studentID"][0]>="n":
            return Student.objects.using('student2').create(**validated_data)
        else:
            return Student.objects.using('student1').create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Student` instance, given the validated data.
        """
        instance.studentID = validated_data.get('studentID', instance.studentID)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.firstName = validated_data.get('firstName', instance.firstName)
        if validated_data["studentID"][0]>="n":
            instance.save(using='student2')
        else:
            instance.save(using='student1')
        return instance

class EnrollSerializer(serializers.Serializer):

    studentID = serializers.CharField(required=False, allow_blank=True, max_length=100)
    courseID  = serializers.CharField(required=True, allow_blank=False, max_length=100)


   
    def create(self, validated_data):
        """
        Create and return a new `Enrollment` instance, given the validated data.
        """
        if validated_data["studentID"][0]>="n":
            return Enrollment.objects.using('student2').create(**validated_data)
        else:
            return Enrollment.objects.using('student1').create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Enrollment` instance, given the validated data.
        """
        instance.courseID = validated_data.get('courseID', instance.courseID)
        instance.studentID = validated_data.get('studentID', instance.studentID)
       
        if validated_data["studentID"][0]>="n":
            instance.save(using='student2')
        else:
            instance.save(using='student1')
        return instance