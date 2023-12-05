import time
from math import trunc

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, SDLK_d, SDLK_s, SDLK_f, SDLK_a, SDLK_UP, get_canvas_width, get_canvas_height

import lose_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import game_world
import game_framework
import t200_play_mode
import server
from server_const import *
import title_mode


class T200Ai:

    def __init__(self):
        self.x, self.y = PLAYER_START_LINE, AI_GROUND
        self.image = load_image('./resource/runner2_sprite_sheet.png')
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.action = 4
        self.frame = 0
        self.speed = 0

        self.build_behavior_tree()

    def get_bb(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 20, sy - 47, sx + 15, sy + 35

    def update(self):
        self.bt.run()

    def draw(self):
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom

        self.image.clip_draw(int(self.frame) * 580, self.action * 510, 580, 510, sx, sy, 100, 100)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'ai:endpoint':
            game_framework.change_mode(lose_mode)

    def run_to_end(self):
        self.action = 2
        self.x += RUN_SPEED_PPS * game_framework.get_frame_time()
        self.frame = (self.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

        return BehaviorTree.RUNNING

    def check_hurdle(self):
        pass

    def do_jump(self):
        pass


    def build_behavior_tree(self):
        a1 = Action('Set random location', self.run_to_end)
        root = Sequence('Run!', a1)
        self.bt = BehaviorTree(root)

