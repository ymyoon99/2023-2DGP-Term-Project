# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_1, SDLK_2
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_font

# Internal_Library
import game_framework
import server
from server_const import *

import title_mode


def init():
    global image
    global font

    image = load_image('./background/leaderboard.jpg')
    font = load_font('./resource/Game.TTF', 35)


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    font.draw(790, 600, f'{server.lap_times[-1]}', (0, 0, 0))
    font.draw(790, 500, f'{server.lap_times[-2]}', (0, 0, 0))
    font.draw(790, 400, f'{server.lap_times[-3]}', (0, 0, 0))
    font.draw(790, 300, f'{server.lap_times[-4]}', (0, 0, 0))
    font.draw(790, 200, f'{server.lap_times[-5]}', (0, 0, 0))
    update_canvas()
    pass


def handle_events(leaderboard=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
