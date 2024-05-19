from django.db import models
from django.utils import timezone

# Create your models here.

class UserRequest(models.Model):
    video = models.FileField(upload_to='videos', blank=True)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)

    def open_video(self):
        return open(self.file_name, 'rb')

    def __str__(self):
        return '%s(%s)' % (self.text, self.id)