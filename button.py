from pico2d import *

import server
from server_const import *


class T200Button:

    def __init__(self):
        self.x, self.y = BUTTON_X_LEFT, BUTTONACTION_Y
        self.image = load_image('./resource/Button.png')
        self.speed = 6
        self.direction = 1
        self.ButtonIndex = False

        self.success = load_wav('./resource/sound/buttonsucc.wav')
        self.success.set_volume(32)

        self.fail = load_wav('./resource/sound/buttonfail.wav')
        self.fail.set_volume(32)

    def update(self):
        self.x += self.speed * self.direction

        if self.x <= BUTTON_X_LEFT:
            self.direction = 1
        elif self.x >= BUTTON_X_RIGHT:
            self.direction = -1

        self.ButtonIndex = False

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.ButtonIndex:
                self.success.play()
                server.t200_runner.stamina += 10
                self.x, self.y = BUTTON_X_LEFT, BUTTONACTION_Y  # 성공할 시 버튼 초기화
            else:
                self.fail.play()
                server.t200_runner.stamina -= 10

    def get_bb(self):
        return self.x - 6, self.y - 45, self.x + 5, self.y + 45

    def handle_collision(self, group, other):
        if group == 'ButtonAction':
            self.ButtonIndex = True


class T400Button:

    def __init__(self):
        self.x, self.y = BUTTON_X_LEFT, BUTTONACTION_Y
        self.image = load_image('./resource/Button.png')
        self.speed = 6
        self.direction = 1
        self.ButtonIndex = False

        self.success = load_wav('./resource/sound/buttonsucc.wav')
        self.success.set_volume(32)

        self.fail = load_wav('./resource/sound/buttonfail.wav')
        self.fail.set_volume(32)

    def update(self):
        self.x += self.speed * self.direction

        if self.x <= BUTTON_X_LEFT:
            self.direction = 1
        elif self.x >= BUTTON_X_RIGHT:
            self.direction = -1

        self.ButtonIndex = False

    def draw(self):
        self.image.draw(self.x, self.y)
        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            if self.ButtonIndex:
                self.success.play()
                server.t400_runner.stamina += 10
                self.x, self.y = BUTTON_X_LEFT, BUTTONACTION_Y  # 성공할 시 버튼 초기화
            else:
                self.fail.play()
                server.t400_runner.stamina -= 10

    def get_bb(self):
        return self.x - 6, self.y - 45, self.x + 5, self.y + 45

    def handle_collision(self, group, other):
        if group == 'ButtonAction':
            self.ButtonIndex = True
