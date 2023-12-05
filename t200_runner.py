from math import trunc

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, SDLK_a, SDLK_UP

import game_framework
import server
import win_mode
from server_const import *


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


def collision(e):
    return e[0] == 'COLLISION'


def isGround(e):
    return e[0] == 'isGround'


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


class Run:

    @staticmethod
    def enter(runner, e):
        runner.stamina -= 1
        if up_down(e):
            runner.action = 2

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.stamina -= 0.15
        if runner.stamina <= 0:
            runner.stamina = 0
            runner.state_machine.handle_event(('COLLISION', 0))  # Transition to Hurt state

        runner.x += (RUN_SPEED_PPS * 1) * game_framework.get_frame_time()
        runner.frame = (runner.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8


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

        runner.x += runner.dir * (RUN_SPEED_PPS / 2) * game_framework.get_frame_time()
        runner.frame = (runner.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 10


class Jump:

    @staticmethod
    def enter(runner, e):
        runner.stamina -= 20
        runner.action = 3
        runner.frame = 0
        runner.animation_done = False

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        if runner.stamina <= 0:
            runner.stamina = 0
            runner.state_machine.handle_event(('COLLISION', 0))

        runner.y += runner.gravity * (JUMP_SPEED_PPS * 0.35) * game_framework.get_frame_time()
        runner.gravity -= 0.16
        runner.x += 1.7

        if runner.y < PLAYER_1_GROUND:
            runner.gravity = 5
            runner.y = PLAYER_1_GROUND
            runner.state_machine.handle_event(('isGround', 0))

        if not runner.animation_done:
            runner.frame = (
                                       runner.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 8
            if int(runner.frame) == 7:
                runner.animation_done = True


class Hurt:

    @staticmethod
    def enter(runner, e):
        runner.stamina += 20
        runner.action = 7
        runner.animation_done = False
        runner.frame = 0
        runner.y = PLAYER_1_GROUND
        runner.hurt_start_time = get_time()
        runner.gravity = 5

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        hurt_check_time = get_time()
        hurt_spend_time = hurt_check_time - runner.hurt_start_time

        if not runner.animation_done:
            runner.frame = (
                                       runner.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * 0.5 * game_framework.get_frame_time()) % 10
            if int(runner.frame) == 9:
                runner.animation_done = True
        else:
            if hurt_spend_time > 2:
                runner.state_machine.handle_event(('TIME_OUT', 0))
                runner.y = PLAYER_1_GROUND  # Y축 보정


class StateMachine:
    def __init__(self, runner):
        self.runner = runner
        self.cur_state = Idle  # 초기 상태
        self.transitions = {
            Idle: {left_down: Walk, right_down: Walk, up_down: Run, a_key_down: Jump},
            Run: {up_up: Idle, left_down: Walk, right_down: Walk, a_key_down: Jump},
            Walk: {left_down: Walk, left_up: Idle, right_down: Walk, right_up: Idle, up_down: Run, a_key_down: Jump},
            Jump: {isGround: Idle},
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

        if e[0] == 'isGround':
            self.cur_state.exit(self.runner, e)
            self.cur_state = Idle
            self.cur_state.enter(self.runner, e)
            return True

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.runner, e)
                self.cur_state = next_state
                self.cur_state.enter(self.runner, e)
                return True

        return False


class Runner:
    def __init__(self):  # Player 초기 상태
        self.x, self.y = PLAYER_START_LINE, PLAYER_1_GROUND  # 초기 위치
        self.frame = 0
        self.action = 4  # 시작 모션
        self.stamina = STAMINA_MAX  # 초기 스태미나 값
        self.dir = 0
        self.image = load_image('./resource/runner1_sprite_sheet.png')
        self.font_time = load_font('./resource/Game.TTF', 40)
        self.font_stamina = load_font('./resource/Game.TTF', 20)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.gravity = 5
        self.start_time = None
        self.hurt_start_time = None

    def update(self):
        self.state_machine.update()
        self.x = clamp(50.0, self.x, server.t200_background.w - 50.0)
        self.y = clamp(50.0, self.y, server.t200_background.h - 50.0)
        self.stamina = clamp(0, self.stamina, STAMINA_MAX + 1)

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):

        sx, sy = self.x - server.t200_background.window_left, self.y - server.t200_background.window_bottom
        self.image.clip_draw(int(self.frame) * 556, self.action * 504, 556, 504, sx, sy, 100, 100)

        # TIME_CHECKER
        if self.start_time is None:
            self.start_time = get_time()
        running_time = get_time() - self.start_time

        minutes, seconds = divmod(running_time, 60)
        running_time_formatted = f'{int(minutes):02d}.{seconds:.03f}'

        self.font_time.draw(10, 600, f'RUNNING TIME: {running_time_formatted}', (0, 0, 0))

        # STAMINA_HEAD_DRAW
        self.font_stamina.draw(sx - 15, sy + 55, f'{trunc(self.stamina):02d}', (60, 179, 113))

        # BB_DRAW
        draw_rectangle(*self.get_bb())

    def get_bb(self):  # 히트 박스
        sx = self.x - server.t200_background.window_left
        sy = self.y - server.t200_background.window_bottom
        return sx - 20, sy - 47, sx + 15, sy + 35

    def handle_collision(self, group, other):
        if group == 'runner:hurdle':
            self.state_machine.handle_event(('COLLISION', 0))
        if group == 'runner:endpoint':
            self.record_lap_time()
            print(server.lap_times[0])
            game_framework.change_mode(win_mode)

    def record_lap_time(self):
        end_time = get_time()
        if self.start_time is not None:
            lap_time = end_time - self.start_time
            lap_time_seconds = round(lap_time, 3)
            minutes, seconds = divmod(lap_time_seconds, 60)

            lap_time_formatted = f'{int(minutes):02d}.{seconds:.03f}'

            server.lap_times.append(('200M', lap_time_formatted))
