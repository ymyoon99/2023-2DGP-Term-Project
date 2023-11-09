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

# time_out = lambda e : e[0] == 'TIME_OUT'


# PLAYER MOVEMENT SETTINGS
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Idle:

    @staticmethod
    def enter(player, e):
        player.action = 4
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.stamina += game_framework.get_frame_time()
        if player.stamina > 99: player.stamina = 100
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.get_frame_time()) % 10
        # if get_time() - player.wait_time > 2:
        #     player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Run:
# 화면에 1부터 3초까지 증가하는 숫자 보이면서, 특정 버튼 입력 이벤트 3초 마다 한번 씩, 실패하거나 더 누르면 넘어짐.
    @staticmethod
    def enter(player, e):
        if right_down(e):  # 오른쪽으로 RUN
            player.dir, player.action, player.face_dir = 1, 2, 1


    @staticmethod
    def exit(player, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.stamina -= game_framework.get_frame_time() * 5
        if player.stamina < 0: player.stamina = 0
        player.x += player.dir * RUN_SPEED_PPS * game_framework.get_frame_time()
        player.x = clamp(25, player.x, 1280 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.get_frame_time()) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Walk:

    @staticmethod
    def enter(player, e):
        if space_down(e):
            player.dir, player.action, player.face_dir = 1, 0, 1


    @staticmethod
    def exit(player, e):
        # if space_down(e):
        #     player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.stamina += game_framework.get_frame_time()
        # if player.stamina > 99: player.stamina = 100
        player.x += player.dir * RUN_SPEED_PPS / 3 * game_framework.get_frame_time()
        player.x = clamp(25, player.x, 1600 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Jump:

    @staticmethod
    def enter(player, e):
        if a_key_down(e):
            player.action, player.face_dir = 3, 1

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.stamina = player.stamina - 50
        if player.stamina > 99: player.stamina = 100
        player.x += player.dir * RUN_SPEED_PPS / 3 * game_framework.get_frame_time()
        player.x = clamp(25, player.x, 1600 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Hurt:

    @staticmethod
    def enter(player, e):
        player.action = 7
        pass


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.stamina = 20
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.get_frame_time()) % 10

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle # 초기 상태
        self.transitions = {
            Idle: {right_down: Run, space_down: Walk},
            Run: {right_up: Idle, space_down: Walk},
            Walk: {space_up: Idle, right_down: Run}
            # Jump: {}
            # Hurt: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
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
    def __init__(self): # Player 초기 상태
        self.x, self.y = 100, 210  # 초기 위치
        self.frame = 0
        self.action = 4  # start motion
        self.face_dir = 1
        self.image = load_image('runner1_sprite_sheet.png')
        self.font_time = load_font('ENCR10B.TTF', 40)
        self.font_stamina = load_font('ENCR10B.TTF', 20)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.stamina = 100 # 초기 스태미나 값
        # self.timer

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()
        self.font_stamina.draw(self.x - 15, self.y + 55, f'{trunc(self.stamina):02d}', (60, 179, 113))
        self.font_time.draw(10, 630, f'Running Time: {get_time():.03f}', (0, 0, 0))
        draw_rectangle(*self.get_bb())
        # x1, y1, x2, y2 == *self.get_bb()


    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 30, self.y + 40
        # 값 4개짜리 Tuple

    def handle_collision(self, group, other):
        pass
