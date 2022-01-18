from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^r/$', views.register, name='register'),
    re_path(r'^c/$', views.command, name='command'),
]
