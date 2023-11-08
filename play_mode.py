import random

from pico2d import *
import game_framework

import game_world
from background import Background
from player import Player


# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player1.handle_event(event)

def init():
    global grass
    global player1

    running = True

    grass = Background()
    game_world.add_object(grass, 0)

    player1 = Player()
    game_world.add_object(player1, 1)

    # zombies = [Zombie() for _ in range(5)]
    # game_world.add_objects(zombies, 1)  # 레이어 1번에 좀비 5마리 추가.

    # 볼을 바닥에 뿌림
    # global balls
    # balls = [Ball(random.randint(100, 1600-100), 60, 0) for _ in range(30)]
    # game_world.add_objects(balls,1)

    # zombies = [Zombie() for _ in range(5)]
    # game_world.add_objects(zombies, 1) # 레이어 1번에 좀비 5마리 추가.

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

