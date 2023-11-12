from pico2d import *
import game_framework


class Endpoint:

    def __init__(self):
        self.x, self.y = 1080, 520
        self.image = load_image('./resource/end_flag.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 16, self.y - 1000, self.x + 23, self.y + 30

    def handle_collision(self, group, other):
        pass


