from django.contrib import admin
from django.urls import path, include

from courses.views import home_index

urlpatterns = [
    path('', home_index, name='home_index'),
    path('courses/', include('courses.urls')),
    path('admin/', admin.site.urls),
]
