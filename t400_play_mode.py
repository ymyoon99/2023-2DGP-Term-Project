import random

from pico2d import *
import game_framework

import game_world
import server
from server_const import *

import title_mode
from t400_background import T400Background
from t400_runner import Runner
from hurdle import T400Hurdle
from ai_hurdle import AiT400Hurdle
from endpoint import T400Endpoint
from t400_ai import T400Ai
from ui import T400Ui
from buttonaction import ButtonAction
from button import T400Button


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            server.t400_runner.handle_event(event)
            server.button.handle_event(event)


def init():
    running = True

    server.t400_background = T400Background()
    game_world.add_object(server.t400_background, 0)

    server.t400_runner = Runner()
    game_world.add_object(server.t400_runner, 2)

    server.t400_hurdle = [T400Hurdle() for _ in range(16)]
    game_world.add_objects(server.t400_hurdle, 1)

    server.t400_ai_hurdle = [AiT400Hurdle() for _ in range(16)]
    game_world.add_objects(server.t400_ai_hurdle, 1)

    server.t400_endpoint = T400Endpoint()
    game_world.add_object(server.t400_endpoint, 1)

    server.ai = T400Ai()
    game_world.add_object(server.ai, 2)

    server.ui = T400Ui()
    game_world.add_object(server.ui, 1)

    server.buttonaction = ButtonAction()
    game_world.add_object(server.buttonaction, 1)

    server.button = T400Button()
    game_world.add_object(server.button, 1)

    # 충돌 상황 등록
    game_world.add_collision_pair('runner:hurdle', server.t400_runner, None)
    for hurdle in server.t400_hurdle:
        game_world.add_collision_pair('runner:hurdle', None, hurdle)

    game_world.add_collision_pair('runner:endpoint', server.t400_runner, None)
    game_world.add_collision_pair('runner:endpoint', None, server.t400_endpoint)

    game_world.add_collision_pair('ai:endpoint', server.ai, None)
    game_world.add_collision_pair('ai:endpoint', None, server.t400_endpoint)

    game_world.add_collision_pair('ButtonAction', server.button, None)
    game_world.add_collision_pair('ButtonAction', None, server.buttonaction)


def finish():
    game_world.clear()
    game_world.clear_collision_pairs()
    T400Hurdle.reset_position(T400Hurdle)
    AiT400Hurdle.reset_position(AiT400Hurdle)
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
