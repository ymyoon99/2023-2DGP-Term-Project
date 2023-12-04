from pico2d import *
from server_const import *


class ButtonAction:

    def __init__(self):
        self.x, self.y = BUTTON_MID, BUTTONACTION_Y
        self.image = load_image('./resource/ButtonMap.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        return self.x - 13, self.y - 48, self.x + 12, self.y + 48

    def handle_collision(self, group, other):
        pass
