from django.test import TestCase
from django.core.files import File
from .models import UserRequest
from .runtext import create_and_delete_runtext_video
from pathlib import Path
import os

# Create your tests here.

class UserRequestTextCase(TestCase):
    def setUp(self): 
        self._text = 'test text'
        with create_and_delete_runtext_video(self._text) as f:
            ur = UserRequest.objects.create(video=File(f, Path(f.name).name), text=self._text)
        self.addCleanup(lambda: os.remove(ur.video.path))


    def test_file_readable(self):
        ur = UserRequest.objects.filter(text=self._text).first()
        ur.video.open('rb')
        ur.video.close()
