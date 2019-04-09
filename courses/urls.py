from django.contrib import admin
from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
  path('fill/', views.fill, name='fill'), 
  path('reset/', views.reset, name='reset'), 
  path('convert/', views.convert, name='convert'),
]
