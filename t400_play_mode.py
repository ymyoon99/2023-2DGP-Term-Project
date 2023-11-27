import random
from pico2d import *


import game_framework
import game_world
import server
from server_const import *

from t400_background import T400_Background
from t400_runner import Runner
from t400_hurdle import Hurdle
from t400_endpoint import Endpoint

# Linked_Mode
import title_mode


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            server.t400_runner.handle_event(event)

def init():

    running = True

    server.t400_background = T400_Background()
    game_world.add_object(server.t400_background, 0)

    server.t400_runner = Runner()
    game_world.add_object(server.t400_runner, 1)

    server.t400_hurdle = [Hurdle() for _ in range(10)]
    game_world.add_objects(server.t400_hurdle, 1)

    server.t400_endpoint = Endpoint()
    game_world.add_object(server.t400_endpoint, 1)

    # 충돌 상황 등록
    game_world.add_collision_pair('runner:hurdle', server.t400_runner, None)
    for hurdle in server.t400_hurdle:
        game_world.add_collision_pair('runner:hurdle', None, hurdle)

    game_world.add_collision_pair('runner:endpoint', server.t400_runner, None)
    game_world.add_collision_pair('runner:endpoint', None, server.t400_endpoint)



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

