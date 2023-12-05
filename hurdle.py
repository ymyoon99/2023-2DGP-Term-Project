from pico2d import *
import random
import game_world
import server
from server_const import *


class T200Hurdle:
    image = None
    hurdle_count = 0  # 허들 객체의 수를 추적하기 위한 클래스 변수

    def __init__(self, x=None, y=None):
        if T200Hurdle.image == None:
            T200Hurdle.image = load_image('./resource/hurdle.png')

        # x 좌표 설정
        if x is None:
            num_hurdles = 8
            interval = 200
            center_x = server.t200_background.w // 2

            # 중심에서부터 200씩 간격을 두고 총 10번 생성
            index = T200Hurdle.hurdle_count
            self.x = center_x + (index * interval) - (num_hurdles * interval // 2)
            T200Hurdle.hurdle_count += 1
        else:
            self.x = x

        self.y = y if y else RUNNER_HURDLE_Y

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 18, sy - 25, sx + 18, sy + 25

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
            if self in game_world.objects[1]:  # 해당 객체가 게임 월드에 있는지 확인
                game_world.remove_object(self)


class T400Hurdle:

    def __init__(self):
        self.image = load_image('./resource/hurdle.png')

        self.x = random.randint(HURDLE_CLAMP, server.t400_background.w - HURDLE_CLAMP)
        self.y = RUNNER_HURDLE_Y

    def update(self):
        pass

    def draw(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        self.image.draw(sx, sy)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def get_bb(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        return sx - 18, sy - 25, sx + 18, sy + 25

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
            if self in game_world.objects[1]:  # 해당 객체가 게임 월드에 있는지 확인
                game_world.remove_object(self)
