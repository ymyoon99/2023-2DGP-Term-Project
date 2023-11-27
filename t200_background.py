from pico2d import *

import server


class T200_Background:
    def __init__(self):
        self.image = load_image('./background/200M.png')

        self.cw = get_canvas_width() # 캔버스의 너비
        self.ch = get_canvas_height() # 캔버스의 높이

        self.w = self.image.w # 실제 이미지의 넓이
        self.h = self.image.h # 실제 이미지의 높이

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = clamp(0, int(server.runner.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(server.runner.y) - self.ch // 2, self.h - self.ch - 1)


    def get_bb(self):
        return 0, 0, 0, 0


