from pico2d import *

import game_framework

import server


class Endpoint:

    def __init__(self):
        self.x, self.y = server.t200_background.w - 160, 520
        # self.image = load_image('./resource/end_flag.png')

    def update(self):
        pass

    def draw(self):
        # self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 16, sy - 1000, sx + 23, sy + 30

    def handle_collision(self, group, other):
        pass


