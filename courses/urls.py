from django.contrib import admin
from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
  path('', views.courses_index, name='courses_index'), 

  path('department', views.api_department_index, name='api_department_index'), 
  path('department/<int:id>', views.api_department_show, name='api_department_show'),
  path('course/<int:id>', views.api_course_show, name='api_course_show'),

  path('solve/', views.solve, name='solve'), 
  path('fill/', views.fill, name='fill'), 
  path('reset/', views.reset, name='reset'), 
  path('convert/', views.convert, name='convert'),
]
