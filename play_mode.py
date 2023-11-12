import random

from pico2d import *
import game_framework

import game_world
import title_mode
from background import Background
from player import Player
from hurdle import Hurdle
from end_line import EndLine


# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            player1.handle_event(event)

def init():
    global grass
    global player1
    global hurdle
    global end_line

    running = True

    grass = Background()
    game_world.add_object(grass, 0)

    player1 = Player()
    game_world.add_object(player1, 1)

    hurdle = [Hurdle() for _ in range(2)]
    game_world.add_objects(hurdle, 1)

    end_line = EndLine()
    game_world.add_object(end_line, 1)

    # #충돌 상황을 등록... boy와 balls들의 충돌 상황을 등록.
    # game_world.add_collision_pair('boy:ball', boy, None)
    # for ball in balls:
    #     game_world.add_collision_pair('boy:ball', None, ball)

    # game_world.add_collision_pair('boy:zombie', boy, None)
    # for zombie in zombies:
    #     game_world.add_collision_pair('boy:zombie', None, zombie)
    #
    # game_world.add_collision_pair('ball:zombie', ball, None)
    # for zombie in zombies:
    #     game_world.add_collision_pair('ball:zombie', None, zombie)



def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions() # 충돌을 업데이트하는 함수

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

