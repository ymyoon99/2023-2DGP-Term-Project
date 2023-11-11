from pico2d import *
import random
import math
import game_framework


class Hurdle:

    def __init__(self):
        self.x, self.y = random.randint(100, 1000), 210
        self.image = load_image('hurdle.png')


    def update(self):
        pass


    def draw(self):
        self.image.draw(self.x, self.y, 10, 10)
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 70, self.y - 50, self.x + 70, self.y + 50

    def handle_collision(self, group, other):
        pass
        # if group == 'ball:zombie':
        #     pass
        # if group == 'boy:zombie':
        #     game_framework.quit()

