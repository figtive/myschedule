from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from . import utils

def home_index(request):
  return render(request, 'home/index.html')

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

