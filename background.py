from pico2d import *

import server


class Background:
    def __init__(self):
        # self.image = load_image('./background/back_ground (1).png')
        self.image = load_image('./background/200M.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)

    def update(self):
        self.window_left = int(server.runner.x) - self.cw // 2
        self.window_bottom = int(server.runner.y) - self.ch // 2

        # 클리핑 영역 계산, 슬라이드의 ?? 좌표.

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)


    def get_bb(self):
        return 0, 0, 0, 0


