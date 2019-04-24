from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.renderers import JSONRenderer

from .models import *
from .serializer import *
from . import utils
from json import loads

from .backtracking import Backtracking

@require_http_methods((["GET"]))
def home_index(request):
  return render(request, 'home/index.html')

@require_http_methods((["GET"]))
def courses_index(request):
  context = loads(api_department_index(request).content)
  return render(request, 'course/index.html', context)

@require_http_methods((["GET"]))
def api_department_index(request):
  json = {'data': []}
  for dep in Department.objects.all():
    serializer = DepartmentSerializer(dep)
    json['data'].append(serializer.data)
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["GET"]))
def api_department_show(request, id):
  json = {}
  serializer = DepartmentSerializer(get_object_or_404(Department, pk=id))
  json['data'] = serializer.data
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["GET"]))
def api_course_show(request, id):
  json = {}
  serializer = CourseSerializer(get_object_or_404(Course, pk=id))
  json['data'] = serializer.data
  return JsonResponse(json, json_dumps_params={'indent': 2})

@require_http_methods((["POST"]))
def solve(request):
  if request.method == 'POST':
    request_body_dict = loads(request.body.decode("utf-8"))
    json = {'data': {'selected': request_body_dict['check']}}
    json['data']['time_preference'] = request_body_dict['time_preference']
    json['data']['density_preference'] = request_body_dict['density_preference']
    bt = Backtracking()
    for course_id in json['data']['selected']:
      course_obj = Course.objects.get(id=course_id)
      bt.add_variable(course_obj, list(course_obj.course_classes.all()))
    bt.add_binary_constraint_to_all(lambda a, b: not a.clash_with(b))

    morning_bool = None
    packed_bool = None
    if request_body_dict['time_preference'] == 'morning':
      morning_bool = True
    if request_body_dict['time_preference'] == 'evening':
      morning_bool = False
    if request_body_dict['density_preference'] == 'packed':
      packed_bool = True
    if request_body_dict['density_preference'] == 'spread':
      packed_bool = False

    result_obj = bt.get_solution(morning_preference=morning_bool, packed_preference=packed_bool)
    result_list = []
    if result_obj:
      json['data']['solution_found'] = True
      for course, class_ in result_obj.items():
        result_list.append({'course':SimpleCourseSerializer(course).data, 'class': CourseClassSerializer(class_).data})
    else:
      json['data']['solution_found'] = False
    json['data']['result'] = result_list
    return JsonResponse(json, json_dumps_params={'indent': 2})

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

