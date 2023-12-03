import random

from pico2d import *
import game_framework

import game_world
import server
from server_const import *

import title_mode
from background import T200_Background
from t200_runner import Runner
from hurdle import T200_Hurdle
from endpoint import T200_Endpoint
from ai import Ai
from ui import StUi


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            server.t200_runner.handle_event(event)


def init():
    running = True

    server.t200_background = T200_Background()
    game_world.add_object(server.t200_background, 0)

    server.t200_runner = Runner()
    game_world.add_object(server.t200_runner, 1)

    server.t200_hurdle = [T200_Hurdle() for _ in range(10)]
    game_world.add_objects(server.t200_hurdle, 1)

    server.t200_endpoint = T200_Endpoint()
    game_world.add_object(server.t200_endpoint, 1)

    server.ai = Ai()
    game_world.add_object(server.ai, 1)

    server.ui = StUi()
    game_world.add_object(server.ui, 1)

    # 충돌 상황 등록
    game_world.add_collision_pair('runner:hurdle', server.t200_runner, None)
    for hurdle in server.t200_hurdle:
        game_world.add_collision_pair('runner:hurdle', None, hurdle)

    game_world.add_collision_pair('runner:endpoint', server.t200_runner, None)
    game_world.add_collision_pair('runner:endpoint', None, server.t200_endpoint)

    game_world.add_collision_pair('ai:endpoint', server.ai, None)
    game_world.add_collision_pair('ai:endpoint', None, server.t200_endpoint)


def finish():
    game_world.clear()
    game_world.clear_collision_pairs()
    del server.t200_hurdle[:]
    pass


def update():
    game_world.update()
    game_world.handle_collisions()  # 충돌을 업데이트하는 함수


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass
