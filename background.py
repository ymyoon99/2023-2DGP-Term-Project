from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('./background/back_ground (1).png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(640, 360)

    def get_bb(self):
        return 0, 0, 1600-1, 0


