from pico2d import *
import random
import math
import game_framework
import game_world
import server

HURDLE_CLAMP = 300

class Hurdle:
    image = None

    def __init__(self, x=None, y=None):
        if Hurdle.image == None:
            self.image = load_image('./resource/hurdle.png')

        # x 좌표 설정
        self.x = x if x else random.randint(HURDLE_CLAMP, server.t200_background.w - HURDLE_CLAMP)
        self.y = y if y else 210-20

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
        return sx - 23, sy - 30, sx + 23, sy + 30

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
             game_world.remove_object(self)

