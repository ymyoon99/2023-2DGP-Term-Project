# 이것은 각 상태들을 객체로 구현한 것임.
import time
from math import trunc

from pico2d import get_time, load_image, load_font, clamp, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, \
    draw_rectangle, SDLK_d, SDLK_s, SDLK_f, SDLK_a

import game_world
import game_framework


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


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


class Idle:

    @staticmethod
    def enter(player, e):
        player.action = 4
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.stamina += game_framework.get_frame_time() * 5
        if player.stamina > 99: player.stamina = 100
        player.frame = (player.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Run:

    @staticmethod
    def enter(player, e):
        player.stamina -= 10
        if right_down(e):
            player.action = 2

    @staticmethod
    def exit(player, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.stamina -= game_framework.get_frame_time() * 10
        if player.stamina < 0: player.stamina = 0
        player.x += RUN_SPEED_PPS * game_framework.get_frame_time()
        player.x = clamp(25, player.x, 1280 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION_8 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Walk:

    @staticmethod
    def enter(player, e):
        if space_down(e):
            player.action = 0

    @staticmethod
    def exit(player, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.stamina += game_framework.get_frame_time()
        if player.stamina > 99: player.stamina = 100
        player.x += RUN_SPEED_PPS / 3 * game_framework.get_frame_time()
        player.x = clamp(25, player.x, 1600 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Jump:

    @staticmethod
    def enter(player, e):
        player.stamina -= 20
        if a_key_down(e):  # 추가된 조건
            player.action = 3
        player.wait_time = get_time()

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if get_time() - player.wait_time < 1:
            player.y += RUN_SPEED_PPS * 1.3 * game_framework.get_frame_time()
            player.x += RUN_SPEED_PPS * 1.5 * game_framework.get_frame_time()
        elif get_time() - player.wait_time >= 1:
            player.y -= RUN_SPEED_PPS * game_framework.get_frame_time()
            player.x += RUN_SPEED_PPS * game_framework.get_frame_time()
            if player.y <= PLAYER_1_GROUND:
                player.state_machine.handle_event(('TIME_OUT', 0))

        player.x = clamp(25, player.x, 1280 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION_10 * 0.2 * game_framework.get_frame_time()) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Hurt:

    @staticmethod
    def enter(player, e):
        player.action = 7
        player.wait_time = get_time()
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        if get_time() - player.wait_time > 2:
            player.state_machine.handle_event(('TIME_OUT', 0))
        player.frame = (player.frame + FRAMES_PER_ACTION_10 * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle  # 초기 상태
        self.transitions = {
            Idle: {right_down: Run, space_down: Walk, a_key_down: Jump},
            Run: {right_up: Idle, space_down: Walk, a_key_down: Jump},
            Walk: {space_up: Idle, right_down: Run, a_key_down: Jump},
            Jump: {a_key_down: Jump, time_out: Idle},
            Hurt: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):

        if self.cur_state == Jump and a_key_down(e): # 2단 점프 방지
            return False

        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)

                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)




class Player:
    def __init__(self):  # Player 초기 상태
        self.x, self.y = PLAYER_START_LINE, PLAYER_1_GROUND  # 초기 위치
        self.frame = 0
        self.action = 4  # 시작 모션
        self.stamina = 100  # 초기 스태미나 값
        self.image = load_image('runner1_sprite_sheet.png')
        self.font_time = load_font('ENCR10B.TTF', 40)
        self.font_stamina = load_font('ENCR10B.TTF', 20)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.jump = 0
        self.can_jump = True


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        self.font_stamina.draw(self.x - 15, self.y + 55, f'{trunc(self.stamina):02d}', (60, 179, 113))
        self.font_time.draw(10, 630, f'Running Time: {get_time():.03f}', (0, 0, 0))
        draw_rectangle(*self.get_bb())

    def get_bb(self):  # 히트 박스
        return self.x - 25, self.y - 50, self.x + 20, self.y + 40

    def handle_collision(self, group, other):
        pass
