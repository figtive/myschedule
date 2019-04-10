from django.contrib import admin
from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
  path('department', views.department_index, name='department_index'), 
  path('department/<int:id>', views.department_show, name='department_show'),
  path('course/<int:id>', views.course_show, name='course_show'),

  path('solve/', views.solve, name='solve'), 
  path('fill/', views.fill, name='fill'), 
  path('reset/', views.reset, name='reset'), 
  path('convert/', views.convert, name='convert'),
]
