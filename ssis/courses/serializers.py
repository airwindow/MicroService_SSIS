from rest_framework import serializers
from courses import models


class CourseSerializer(serializers.Serializer):

    # class Meta:
    #     model = Student
    #     fields = ('studentID', 'lastName', 'firstName')


    courseID = serializers.CharField(required=True, allow_blank=False, max_length=100)
    courseTitle = serializers.CharField(required=False, allow_blank=True, max_length=100)
    roomNum = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self, validated_data):
        """
        Create and return a new `Student` instance, given the validated data.
        """
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Student` instance, given the validated data.
        """
        instance.courseID = validated_data.get('courseID', instance.courseID)
        instance.courseTitle = validated_data.get('courseTitle', instance.courseTitle)
        instance.roomNum = validated_data.get('roomNum', instance.roomNum)

        instance.save()
        return instance
