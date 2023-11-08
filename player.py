# 이것은 각 상태들을 객체로 구현한 것임.

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
        player.dir = 0
        player.frame = 0
        pass

    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.fire_ball()
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        # if get_time() - player.wait_time > 2:
        #     player.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)


class Run:

    @staticmethod
    def enter(player, e):
        if right_down(e):  # 오른쪽으로 RUN
            player.dir, player.action, player.face_dir = 1, 2, 1


    @staticmethod
    def exit(player, e):
        if space_down(e):
            player.fire_ball()

        pass

    @staticmethod
    def do(player):
        # boy.frame = (boy.frame + 1) % 8
        player.x += player.dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(25, player.x, 1600 - 25)
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 556, player.action * 504, 556, 504, player.x, player.y, 100, 100)




class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, right_up: Run, time_out: Idle, space_down: Idle},
            Run: {right_down: Idle, right_up: Idle, space_down: Run},

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
    def __init__(self):
        self.x, self.y = 100, 210  # 초기 위치
        self.frame = 0
        self.action = 4  # start motion
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('player1_sheet.png')
        self.font_time = load_font('ENCR10B.TTF', 40)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        # self.timer

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))


    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x - 10, self.y + 50, f'{self.timer:02d}', (255, 255, 0))
        self.font_time.draw(10, 630, f'Running Time: {get_time():.03f}', (0, 0, 0))
        draw_rectangle(*self.get_bb())
        # x1, y1, x2, y2 == *self.get_bb()

    # fill here
    def get_bb(self):
        return self.x - 25, self.y - 50, self.x + 25, self.y + 50
        # 값 4개짜리 Tuple로 바운딩 박스 값을 나타냄.

    def handle_collision(self, group, other):
        pass
