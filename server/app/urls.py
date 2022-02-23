from app import views
from django.urls import path
from .views import ClientDetailView, ClientListView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('clients/', login_required(ClientListView.as_view()), name='clients'),
    path('clients/<int:client_id>', login_required(ClientDetailView.as_view()), name='clientdetails'),
    path('<int:client_id>/initial', views.initial, name='initial'),
    path('<int:client_id>/report', views.report, name='report'),
    path('upload/', login_required(views.upload), name='upload'),
    path('uploads/', login_required(views.list_uploads), name='uploads'),
    path('uploads/<int:upload_id>', login_required(views.delete_upload), name='upload_detail'),
]
