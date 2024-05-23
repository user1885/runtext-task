from django.test import TestCase
from django.core.files import File
from .models import UserRequest
from .runtext import create_runtext_video
import os

# Create your tests here.

class UserRequestTextCase(TestCase):
    def setUp(self): 
        self._text = 'test text'
        fp = create_runtext_video(self._text)
        print(fp)
        with open(fp, 'rb') as f:
            UserRequest.objects.create(video=File(f, f.name), text=self._text)
        self.addCleanup(lambda: os.remove(fp))

    def test_file_readable(self):
        ur = UserRequest.objects.filter(text=self._text).first()
        print(ur.video.path)
        # ur.video.open('rb')
        # ur.video.close()
