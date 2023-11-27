import random

from pico2d import *
import game_framework

import game_world
import server
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
            server.runner.handle_event(event)

def init():

    running = True

    server.background = Background()
    game_world.add_object(server.background, 0)

    server.runner = Runner()
    game_world.add_object(server.runner, 1)

    server.hurdle = [Hurdle() for _ in range(10)]
    game_world.add_objects(server.hurdle, 1)

    server.endpoint = Endpoint()
    game_world.add_object(server.endpoint, 1)

    # 충돌 상황 등록
    game_world.add_collision_pair('runner:hurdle', server.runner, None)
    for hurdle in server.hurdle:
        game_world.add_collision_pair('runner:hurdle', None, hurdle)

    game_world.add_collision_pair('runner:endpoint', server.runner, None)
    game_world.add_collision_pair('runner:endpoint', None, server.endpoint)



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

