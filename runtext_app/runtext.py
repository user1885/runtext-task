import cv2
from contextlib import contextmanager
from dataclasses import dataclass, field
from django.conf import settings
from ffmpeg import FFmpeg
from tempfile import mkstemp
import traceback
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from ffmpeg import FFmpeg
import os


@dataclass
class RunTextVideo:
    fps: int
    duration: float
    video_size: tuple
    
    bg_color: tuple
    save_to_dir: str
    
    font_path: str
    font_size: int
    font_color: tuple
    
    video_ext: str = os.extsep + 'mp4'
    source_codec: str = 'mp4v'
    target_codec: str = 'avc1'

    def __post_init__(self):
        self.width, self.height = self.video_size
        # Имитация lazy объекта
        self.font = None
        
    def _load_font(self):
        if self.font is None:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        return self.font

    def create(self, text):
        if not os.path.exists(self.save_to_dir):
            os.makedirs(self.save_to_dir)

        _, source_file_path = mkstemp(suffix=self.video_ext)

        out = cv2.VideoWriter(
            source_file_path,
            cv2.VideoWriter_fourcc(*self.source_codec), 
            self.fps, 
            self.video_size)

        total_fps = self.fps * self.duration
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Спавним текст по центру, учитывая размер текста
        x, y = self.width // 2, self.height // 2 - self.font_size / 2
        
        # Считаем скорость, основываясь на длине строки
        text_len = self._load_font().getlength(text)
        speed_x = text_len / total_fps
        
        for _ in range(total_fps):
            frame.fill(0)
            x -= speed_x
            frame_image = Image.new('RGB', self.video_size, color=self.bg_color)
            draw = ImageDraw.Draw(frame_image)
            draw.text((x, y), text, font=self._load_font(), fill=self.font_color)
            frame = np.array(frame_image)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)
        out.release()

        _, target_file_path = mkstemp(suffix=self.video_ext)
        try:
            ffmpeg = (
                FFmpeg().
                option('y').
                input(source_file_path).
                output(target_file_path, vcodec='libx264')
            )
            ffmpeg.execute()
        except:
            traceback.print_exc()
        finally:
            os.remove(source_file_path)

        return target_file_path

# Prebound объект с данными из условия задания
_inst = RunTextVideo(fps=100,
                     duration=3,
                     video_size=(100, 100),
                     save_to_dir='temp',
                     font_path=settings.BASE_DIR / 'static' / 'fonts' / 'CascadiaCodePL-Regular.otf',
                     font_size=60,
                     font_color=(255, 255, 255),
                     bg_color=(243,39,241))

# Prebound функция
def create_runtext_video(text):
    return _inst.create(text)

@contextmanager
def create_and_delete_runtext_video(text):
    fp = create_runtext_video(text)
    f = open(fp, 'rb')
    try:
        yield f
    finally:
        f.close()
        os.remove(fp)
