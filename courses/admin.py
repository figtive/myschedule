from django.contrib import admin

from .models import Course, CourseClass, Lecturer, Meeting, Department

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CourseClass)
admin.site.register(Lecturer)
admin.site.register(Meeting)