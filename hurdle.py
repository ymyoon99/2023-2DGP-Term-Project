from pico2d import *
import random
import math
import game_framework
import game_world
import server


class Hurdle:
    image = None

    def __init__(self, x=None, y=None):
        if Hurdle.image == None:
            self.image = load_image('./resource/hurdle.png')

        # 허들의 최소 간격
        min_distance = 300
        hurdle_clamp = 300

        # x 좌표 설정
        self.x = x if x else random.randint(min_distance, server.background.image.w - hurdle_clamp)
        self.y = y if y else 210-20

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.background.window_left
        sy = self.y - server.background.window_bottom
        return sx - 23, sy - 30, sx + 23, sy + 30

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
             game_world.remove_object(self)

