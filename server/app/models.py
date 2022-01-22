from django.db import models
from django.utils import timezone
import datetime

class Client(models.Model):
    user = models.ManyToManyField(User, on_delete=models.CASCADE, related_name='user', null=True)
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
        cmd.timestamp = datetime.now()
        cmd.save()

    def is_online(self):
        return(datetime.now() - self.last_online) < 10

class Command(models.Model):
    client = models.ForeignKey(Client, related_name='client', on_delete=models.CASCADE)
    cmdline = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
