import time
from math import trunc

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, SDLK_d, SDLK_s, SDLK_f, SDLK_a, SDLK_UP, get_canvas_width, get_canvas_height

import game_world
import game_framework
import t200_play_mode
import server
from server_const import *
import title_mode


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def space_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


def a_key_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_key_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


<<<<<<< HEAD
# PLAYER MOVEMENT SETTINGS
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_8 = 8
FRAMES_PER_ACTION_10 = 10

PLAYER_1_GROUND = 210
PLAYER_START_LINE = 100

STAMINA_MAX = 100000000000


=======
>>>>>>> 72815de90f4fa502183efd0ab5d21d2cd19c0494
class Idle:

    @staticmethod
    def enter(runner, e):
        runner.action = 4
        runner.frame = 0
        pass

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.stamina += game_framework.get_frame_time() * 5
        if runner.stamina > STAMINA_MAX - 1: runner.stamina = STAMINA_MAX
        runner.frame = (runner.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    # @staticmethod
    # def draw(runner):
    #     runner.image.clip_draw(int(runner.frame) * 556, runner.action * 504, 556, 504, runner.x, runner.y, 100, 100)


class Run:

    @staticmethod
    def enter(runner, e):
        runner.stamina -= 5
        if up_down(e):
            runner.action = 2

    @staticmethod
    def exit(runner, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(runner):
        runner.stamina -= game_framework.get_frame_time() * 20
        if runner.stamina <= 0:
            runner.stamina = 0
            runner.state_machine.handle_event(('COLLISION', 0))  # Transition to Hurt state
        else:
            runner.x += RUN_SPEED_PPS * game_framework.get_frame_time()
            runner.frame = (runner.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    # @staticmethod
    # def draw(runner):
    #     runner.image.clip_draw(int(runner.frame) * 556, runner.action * 504, 556, 504, runner.x, runner.y, 100, 100)


class Walk:

    @staticmethod
    def enter(runner, e):
        if right_down(e):
            runner.action = 0
            runner.dir = 1
        if left_down(e):
            runner.action = 0
            runner.dir = -1

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.stamina += game_framework.get_frame_time()
        if runner.stamina > STAMINA_MAX - 1: runner.stamina = STAMINA_MAX
        runner.x += runner.dir * RUN_SPEED_PPS / 3 * game_framework.get_frame_time()
        runner.frame = (runner.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    # @staticmethod
    # def draw(runner):
    #     runner.image.clip_draw(int(runner.frame) * 556, runner.action * 504, 556, 504, runner.x, runner.y, 100, 100)


class Jump:

    @staticmethod
    def enter(runner, e):
        runner.stamina -= 20
        if a_key_down(e):  # 추가된 조건
            runner.action = 3
        # runner.wait_time = get_time()
        runner.frame = 0
        runner.animation_done = False

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        if runner.isJump > 0:

            if runner.velocity > 0:
                F = (0.5 * runner.mass * (runner.velocity * runner.velocity))
            else:
                F = -(0.5 * runner.mass * (runner.velocity * runner.velocity))

            runner.y += round(F)
            runner.velocity -= 1
            runner.x += 1

            if runner.y < PLAYER_1_GROUND:
                runner.y = PLAYER_1_GROUND
                runner.isJump = 0
                runner.velocity = 5

        if not runner.animation_done:
            runner.frame = (runner.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 8
            if int(runner.frame) == 7:
                runner.animation_done = True

    # @staticmethod
    # def draw(runner):
    #     runner.image.clip_draw(int(runner.frame) * 556, runner.action * 504, 556, 504, runner.x, runner.y, 100, 100)


class Hurt:

    @staticmethod
    def enter(runner, e):
        runner.stamina += 20
        runner.action = 7
        runner.wait_time = get_time()
        runner.animation_done = False
        runner.frame = 0

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        if not runner.animation_done:
            runner.frame = (runner.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 10
            if int(runner.frame) == 9:
                runner.animation_done = True
        else:
            if get_time() - runner.wait_time > 2:
                runner.state_machine.handle_event(('TIME_OUT', 0))
                runner.y = PLAYER_1_GROUND  # Y축 보정

    # @staticmethod
    # def draw(runner):
    #     runner.image.clip_draw(int(runner.frame) * 556, runner.action * 504, 556, 504, runner.x, runner.y, 100, 100)


class StateMachine:
    def __init__(self, runner):
        self.runner = runner
        self.cur_state = Idle  # 초기 상태
        self.transitions = {
            Idle: {left_down: Walk, right_down: Walk, up_down: Run, a_key_down: Jump},
            Run: {up_up: Idle, left_down: Walk, right_down: Walk, a_key_down: Jump},
            Walk: {left_up: Idle, right_up: Idle, up_down: Run, a_key_down: Jump},
            Jump: {time_out: Idle},
            Hurt: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.runner, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.runner)

    def handle_event(self, e):

        if self.cur_state == Jump and a_key_down(e):  # 2단 점프 방지
            return False

        if e[0] == 'COLLISION':
            self.cur_state.exit(self.runner, e)
            self.cur_state = Hurt
            self.cur_state.enter(self.runner, e)
            return True

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.runner, e)
                self.cur_state = next_state
                self.cur_state.enter(self.runner, e)

                return True

        return False

    # def draw(self):
    #     self.cur_state.draw(self.runner)


class Runner:
    def __init__(self):  # Player 초기 상태
        self.x, self.y = PLAYER_START_LINE, PLAYER_1_GROUND  # 초기 위치
        self.frame = 0
        self.action = 4  # 시작 모션
        self.stamina = STAMINA_MAX  # 초기 스태미나 값
        self.dir = 0
        self.image = load_image('./resource/runner1_sprite_sheet.png')
        self.font_time = load_font('./resource/ENCR10B.TTF', 40)
        self.font_stamina = load_font('./resource/ENCR10B.TTF', 20)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.isJump = 0
        self.velocity = 5
        self.mass = 2

    def jump(self, o):
        self.isJump = 0

    def update(self):
        self.state_machine.update()
        self.x = clamp(50.0, self.x, server.t200_background.w - 50.0)
        self.y = clamp(50.0, self.y, server.t200_background.h - 50.0)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        sx, sy = self.x - server.t200_background.window_left, self.y - server.t200_background.window_bottom
        self.image.clip_draw(int(self.frame) * 556, self.action * 504, 556, 504, sx, sy, 100, 100)

        # NUM_DRAW
        self.font_stamina.draw(sx - 15, sy + 55, f'{trunc(self.stamina):02d}', (60, 179, 113))
        self.font_time.draw(10, 530, f'Stamina: {trunc(self.stamina):02d}', (255, 0, 0))
        self.font_time.draw(10, 630, f'Running Time: {get_time():.03f}', (0, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):  # 히트 박스
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 25, sy - 50, sx + 20, sy + 40

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
            self.state_machine.handle_event(('COLLISION', 0))
        if group == 'runner:endpoint':
            # game_framework.change_mode(title_mode)
            pass
