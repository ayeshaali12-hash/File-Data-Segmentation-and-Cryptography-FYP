from django.db import models
# Create your models here.
import datetime
class MyFileUpload(models.Model):
    file_name = models.CharField(max_length=50)
    file_size = models.CharField(max_length=10,default=0)
    user = models.CharField(max_length=50,default='null')
    hostdata = models.CharField(max_length=50,default='null')
    downloadcount = models.CharField(default=0, max_length=10)
    start_time = models.DateTimeField(default=datetime.datetime.now)
    end_time = models.DateTimeField(default=datetime.datetime.now)
    download_start_time = models.DateTimeField(default=datetime.datetime.now)
    download_end_time = models.DateTimeField(default=datetime.datetime.now)
    del_start_time = models.DateTimeField(default=datetime.datetime.now)
    del_end_time = models.DateTimeField(default=datetime.datetime.now)
    status = models.CharField(max_length=10,default='Uploaded')
    mode = models.CharField(max_length=10,default='Non-Encrypted')
    progress = models.CharField(max_length=10,default=0)
#

class fileData(models.Model):
    LastFileID = models.CharField(max_length=1000000000000)


class ServerData(models.Model):
    assignedID = models.CharField(max_length=10)
    hostname = models.CharField(max_length=50)
    user = models.CharField(max_length=50,default='null')
    password = models.CharField(max_length=50)
    portno = models.CharField(max_length=50)
    status = models.CharField(max_length=10,default="Enabled")


class UserStorage(models.Model):
    user = models.CharField(max_length=50, default='null')
    is_loggedin = models.BooleanField(default=0)
    storage_consumed = models.CharField(max_length=10, default=0)
    storage_alloted = models.CharField(max_length=10, default=1024)

