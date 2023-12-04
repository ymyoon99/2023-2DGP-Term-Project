from pico2d import *

import game_framework

import server
from server_const import *


class Button:

    def __init__(self):
        self.x, self.y = BUTTON_X_LEFT, BUTTONACTION_Y
        self.image = load_image('./resource/Button.png')
        self.speed = 2
        self.direction = 1

    def update(self):
        self.x += self.speed * self.direction

        # 왼쪽 끝에 도달하면 방향을 반대로 변경
        if self.x <= BUTTON_X_LEFT:
            self.direction = 1
        # 오른쪽 끝에 도달하면 방향을 반대로 변경
        elif self.x >= BUTTON_X_RIGHT:
            self.direction = -1

    def draw(self):

        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):

        return self.x - 13, self.y - 48, self.x + 12, self.y + 48

    def handle_collision(self, group, other):
        if group == 'ButtonAction':
            server.ButtonIndex = True