from pico2d import *
import random
import math
import game_framework
import game_world
import server

HURDLE_CLAMP = 300

class Hurdle:


    def __init__(self):

        self.image = load_image('./resource/hurdle.png')

        self.x = random.randint(HURDLE_CLAMP, server.t400_background.w - HURDLE_CLAMP)
        self.y = 210-20

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
        return sx - 23, sy - 30, sx + 23, sy + 30

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
             game_world.remove_object(self)

