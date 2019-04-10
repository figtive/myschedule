from rest_framework import serializers

from .models import *

class MeetingSerializer(serializers.ModelSerializer):
  start_time = serializers.TimeField(format="%H.%M")
  end_time = serializers.TimeField(format="%H.%M")

  class Meta:
    model = Meeting
    fields = (
      'id', 'day', 'start_time', 'end_time', 'class_room'
    )

class LecturerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Lecturer
    fields = (
      'id', 'name'
    )

class CourseClassSerializer(serializers.ModelSerializer):
  lecturers = LecturerSerializer(many=True, read_only=True)
  meetings = MeetingSerializer(many=True, read_only=True)
  language = serializers.CharField(source='get_language_display')

  class Meta:
    model = CourseClass
    fields = (
      'id', 'language', 
      'lecturers', 'meetings'
    )

class CoursePrerequisiteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = (
      'id', 'course_code', 'course_name'
    )

class CourseSerializer(serializers.ModelSerializer):
  prerequisites = CoursePrerequisiteSerializer(many=True, read_only=True)
  course_classes = CourseClassSerializer(many=True, read_only=True)

  class Meta:
    model = Course
    fields = (
      'id', 'course_code', 'course_name', 'sks', 'term', 
      'curriculum', 'prerequisites', 'course_classes'
    )

class DepartmentSerializer(serializers.ModelSerializer):
  courses = CourseSerializer(many=True, read_only=True)

  class Meta:
    model = Department
    fields = ('id', 'name', 'courses')