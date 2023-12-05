import time
from math import trunc

from pico2d import load_image, draw_rectangle

import lose_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import game_framework
import server
from server_const import *


class T400Ai:

    def __init__(self):
        self.x, self.y = PLAYER_START_LINE, AI_GROUND
        self.image = load_image('./resource/runner2_sprite_sheet.png')
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.action = 4
        self.frame = 0
        self.speed = 0
        self.build_behavior_tree()
        self.gravity = 5
        self.jump_x_locations = [6370 + i * 200 for i in range(16)] + [12200]
        self.jx = 0.0
        self.loc_no = 0
        self.now_Jump = False

    def get_bb(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom
        return sx - 20, sy - 47, sx + 15, sy + 35

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 8

        if self.now_Jump:
            self.do_jump()
        elif self.x >= self.jump_x_locations[self.loc_no]:
            self.get_jump_x()
            self.now_Jump = True
        else:
            self.run_to_end()

    def draw(self):
        sx = self.x - server.t400_background.window_left
        sy = self.y - server.t400_background.window_bottom

        self.image.clip_draw(int(self.frame) * 580, self.action * 510, 580, 510, sx, sy, 100, 100)

        # draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'ai:endpoint':
            game_framework.change_mode(lose_mode)

    def run_to_end(self):
        if not self.now_Jump:
            self.action = 2
            self.x += RUN_SPEED_PPS * game_framework.get_frame_time() * 0.8
            self.frame = (self.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    def do_jump(self):
        self.action = 3
        self.frame = (self.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 8
        self.y += self.gravity * (JUMP_SPEED_PPS * 0.35) * game_framework.get_frame_time()
        self.gravity -= 0.16
        self.x += 1.7

        if self.y < AI_GROUND:
            self.gravity = 5
            self.y = AI_GROUND
            self.now_Jump = False
            self.frame = 0

    def get_jump_x(self):
        # 다음 점프 좌표 설정
        self.jx = self.jump_x_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.jump_x_locations)

    def is_front_hurdle(self):
        # 현재 좌표가 점프 좌표와 거의 같으면 성공
        if trunc(self.x) == self.jx:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self):
        a1 = Action('Run to endpoint', self.run_to_end)
        a2 = Action('Do Jump', self.do_jump)
        a3 = Action('Get jump point', self.get_jump_x)

        c1 = Condition('Check Coordinates', self.is_front_hurdle)

        SEQ_run_and_jump = Sequence('특정 좌표에서 점프', a3, c1, a2)

        root = Sequence('AI Behavior', a1, SEQ_run_and_jump)

        self.bt = BehaviorTree(root)
