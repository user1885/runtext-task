from django.core.files import File
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserRequest
from .runtext import create_runtext_video
import traceback

# Create your views here.

def index(request):
    return HttpResponseRedirect('runtext')


class RuntextView(TemplateView):
    template_name = 'runtext_app/index.html'

    def get(self, request):
        data = request.GET
        text = data.get('text')
        if text and not text.isspace():
            text = text.strip()
            # Создаем видео
            file_path, file_name= create_runtext_video(text)
            try:
                with open(file_path, 'rb') as file:
                    response = HttpResponse(file.read(), content_type='video/mp4')
                    response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
                    user_request = UserRequest(
                        text=text, video=File(file, name=file_name))
                    user_request.save()
                return response
            except:
                # Сообщаем об ошибке
                traceback.print_exc()
                return super().get(request, error_msg='Что-то пошло не так!')
        return super().get(request)            
