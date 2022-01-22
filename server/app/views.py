import json
import base64
import os
from datetime import datetime
import tempfile
import shutil

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Command
from .utils import geolocate
from .forms import RegisterUserForm

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

    return render(request, 'register.html', {'form':form})

@login_required
def list_clients(request):
    clients = Client.objects.all().order_by('date')
    return render(request, 'clients.html', {'clients':clients})

@login_required
def client_details(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'client_detailed.html', {'client':client})

@login_required
def masscmd(request):
