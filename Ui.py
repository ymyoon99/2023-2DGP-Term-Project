from pico2d import *
import random
import math
import game_framework
import game_world
import server
from server_const import *


class StUi:

    def __init__(self, x=None, y=None):
        self.images = [load_image(f'./resource/percent/percent_{i}.png') for i in range(0, 110, 10)]

        # x 좌표 설정
        self.x = x if x else 250
        self.y = y if y else 650

    def update(self):
        pass

    def draw(self):
        image_index = int(server.t200_runner.stamina / 10)  # 0부터 100까지 10 단위로 이미지가 있음
        image_index = min(10, max(0, image_index))  # 인덱스가 0 이상 10 미만이 되도록 보정
        image = self.images[image_index]

        image.draw(self.x, self.y)

    def handle_event(self, event):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass
