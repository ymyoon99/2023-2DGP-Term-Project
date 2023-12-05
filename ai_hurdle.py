from pico2d import *
import random
import game_world
import server
from server_const import *


class AiT200Hurdle:
    image = None
    hurdle_count = 0  # 허들 객체의 수를 추적하기 위한 클래스 변수

    def __init__(self, x=None, y=None):
        if AiT200Hurdle.image is None:
            AiT200Hurdle.image = load_image('./resource/hurdle.png')

        # x 좌표 설정
        if x is None:
            interval = 200
            center_x = server.t200_background.w // 2

            # 중심에서부터 200씩 간격을 두고
            self.x = center_x + (AiT200Hurdle.hurdle_count * interval)
            AiT200Hurdle.hurdle_count += 1
        else:
            self.x = x

        self.y = y if y else AI_HURDLE_Y

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 18, sy - 25, sx + 18, sy + 25

    def handle_collision(self, group, other):
        pass

    def reset_position(self):
        interval = 200
        center_x = server.t200_background.w // 2
        AiT200Hurdle.hurdle_count = 0
        self.x = center_x + (AiT200Hurdle.hurdle_count * interval)
        AiT200Hurdle.hurdle_count += 1


class AiT400Hurdle:
    image = None
    hurdle_count = 0  # 허들 객체의 수를 추적하기 위한 클래스 변수

    def __init__(self, x=None, y=None):
        if AiT400Hurdle.image is None:
            AiT400Hurdle.image = load_image('./resource/hurdle.png')

        # x 좌표 설정
        if x is None:
            interval = 200
            center_x = server.t400_background.w // 2

            # 중심에서부터 200씩 간격을 두고
            self.x = center_x + (AiT400Hurdle.hurdle_count * interval)
            AiT400Hurdle.hurdle_count += 1
        else:
            self.x = x

        self.y = y if y else AI_HURDLE_Y

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        return sx - 18, sy - 25, sx + 18, sy + 25

    def handle_collision(self, group, other):
        pass

    def reset_position(self):
        interval = 200
        center_x = server.t400_background.w // 2
        AiT400Hurdle.hurdle_count = 0
        self.x = center_x + (AiT400Hurdle.hurdle_count * interval)
        AiT400Hurdle.hurdle_count += 1
