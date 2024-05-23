import cv2
from dataclasses import dataclass
from django.conf import settings
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os
import uuid


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
    
    def __post_init__(self):
        self.width, self.height = self.video_size
        # Имитация lazy объекта
        self.font = None
        
    def _load_font(self):
        if self.font is None:
            self.font = ImageFont.truetype(self.font_path, self.font_size)
        return self.font

    def create(self, text) -> str:
        if not os.path.exists(self.save_to_dir):
            os.makedirs(self.save_to_dir)
        video_id = uuid.uuid4()
        file_name = '%s.mp4' % video_id
        file_path = os.path.join(self.save_to_dir, file_name)
        out = cv2.VideoWriter(
            file_path,
            cv2.VideoWriter_fourcc(*'mp4v'), 
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
        return file_path, file_name

# Prebound объект с данными из условия задания
_inst = RunTextVideo(fps=100,
                     duration=3,
                     video_size=(100, 100),
                     save_to_dir=settings.MEDIA_ROOT / 'videos',
                     font_path=settings.BASE_DIR / 'static' / 'fonts' / 'CascadiaCodePL-Regular.otf',
                     font_size=60,
                         font_color=(255, 255, 255),
                     bg_color=(243,39,241))

# Prebound функция
def create_runtext_video(text):
    return _inst.create(text)
