from django.db import models
from django.utils.timezone import now

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    created_datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
