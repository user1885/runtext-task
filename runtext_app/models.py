from django.db import models
from django.utils import timezone

# Create your models here.

class UserRequest(models.Model):
    file_name = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s(%s)' % (self.text, self.id)