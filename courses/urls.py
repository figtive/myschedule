from django.contrib import admin
from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
  path('filldb/', views.fill_course_data_to_db, name='fill_course_data_to_db')
]
