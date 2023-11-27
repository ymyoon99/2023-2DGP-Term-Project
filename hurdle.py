from pico2d import *
import random
import math
import game_framework
import game_world


class Hurdle:

    def __init__(self):
        self.x, self.y = random.randint(300, 1000), 210-20
        self.image = load_image('./resource/hurdle.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 23, self.y - 30, self.x + 23, self.y + 30

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
             game_world.remove_object(self)

