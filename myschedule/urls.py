from django.contrib import admin
from django.urls import path

from courses.views import home_index

urlpatterns = [
    path('', home_index, name='home_index'),
    path('admin/', admin.site.urls),
]
