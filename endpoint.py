from pico2d import *

import server
from server_const import *


class T200Endpoint:

    def __init__(self):
        self.x, self.y = server.t200_background.w - ENDPOINT_X_CLAMP, ENDPOINT_Y
        # self.image = load_image('./resource/end_flag.png')

    def update(self):
        pass

    def draw(self):
        # self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 16, sy - 500, sx + 23, sy + 30

    def handle_collision(self, group, other):
        pass


class T400Endpoint:

    def __init__(self):
        self.x, self.y = server.t400_background.w - ENDPOINT_X_CLAMP, ENDPOINT_Y
        # self.image = load_image('./resource/end_flag.png')

    def update(self):
        pass

    def draw(self):
        # self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        return sx - 16, sy - 500, sx + 23, sy + 30

    def handle_collision(self, group, other):
        pass
