from django.db import models
from django.utils import timezone
import datetime

class Client(models.Model):
    id = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    last_online = models.CharField(max_length=100)
    operating_system = models.CharField(max_length=100)
    remote_ip = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
