from pico2d import *
import random
import math
import game_framework
import game_world
import server
from server_const import *


class T200_Hurdle:
    image = None

    def __init__(self, x=None, y=None):
        if T200_Hurdle.image == None:
            self.image = load_image('./resource/hurdle.png')

        # x 좌표 설정
        self.x = x if x else random.randint(HURDLE_CLAMP, server.t200_background.w - HURDLE_CLAMP)
        self.y = y if y else RUNNER_HURDLE_Y

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
        if group == 'runner:hurdle':
            if self in game_world.objects[1]:  # 해당 객체가 게임 월드에 있는지 확인
                game_world.remove_object(self)


class T400_Hurdle:

    def __init__(self):
        self.image = load_image('./resource/hurdle.png')

        self.x = random.randint(HURDLE_CLAMP, server.t400_background.w - HURDLE_CLAMP)
        self.y = RUNNER_HURDLE_Y

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
        if group == 'runner:hurdle':
            game_world.remove_object(self)
