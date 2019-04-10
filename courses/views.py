from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.renderers import JSONRenderer

from .models import *
from .serializer import *
from . import utils

@require_http_methods((["GET"]))
def home_index(request):
  return render(request, 'home/index.html')

@require_http_methods((["GET"]))
def department_index(request):
  json = {'data': []}
  for dep in Department.objects.all():
    serializer = DepartmentSerializer(dep)
    json['data'].append(serializer.data)
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["GET"]))
def department_show(request, id):
  json = {}
  serializer = DepartmentSerializer(get_object_or_404(Department, pk=id))
  json['data'] = serializer.data
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["GET"]))
def course_show(request, id):
  json = {}
  serializer = CourseSerializer(get_object_or_404(Course, pk=id))
  json['data'] = serializer.data
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["POST"]))
def solve(request):
  pass

def fill(request):
  if request.user.is_superuser:
    return HttpResponse(utils.fill_all_course_data_to_db())
  else:
    return HttpResponseForbidden()
  
def reset(request):
  if request.user.is_superuser:
    return HttpResponse(utils.reset_db())
  else:
    return HttpResponseForbidden()

def convert(request):
  if request.user.is_superuser:
    return HttpResponse(utils.SiakParser.convert_all_html_to_json())
  else:
    return HttpResponseForbidden()

