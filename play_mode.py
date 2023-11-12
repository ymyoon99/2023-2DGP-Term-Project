import random

from pico2d import *
import game_framework

import game_world
import title_mode
from background import Background
from runner import Runner
from hurdle import Hurdle
from endpoint import Endpoint


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
    global background
    global player1
    global endpoint

    running = True

    background = Background()
    game_world.add_object(background, 0)

    player1 = Runner()
    game_world.add_object(player1, 1)

    hurdles = [Hurdle() for _ in range(2)]
    game_world.add_objects(hurdles, 1)

    endpoint = Endpoint()
    game_world.add_object(endpoint, 1)

    # 충돌 상황 등록
    game_world.add_collision_pair('player1:hurdle', player1, None)
    for hurdle in hurdles:
        game_world.add_collision_pair('player1:hurdle', None, hurdle)

    game_world.add_collision_pair('player1:endpoint', player1, None)
    game_world.add_collision_pair('player1:endpoint', None, endpoint)



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

