from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

def home_index(request):
  return render(request, 'home/index.html')

def fill_course_data_to_db(request):
  if request.user.is_superuser:
    return HttpResponse('you are a super user!')
  else:
    return HttpResponseForbidden()