# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1, SDLK_2
from pico2d import get_events, load_image, clear_canvas, update_canvas

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import title_mode
import t200_play_mode
import t400_play_mode


def init():
    global image

    image = load_image('./resource/tracklist.jpg')


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    update_canvas()
    pass


def handle_events(tracklist=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            game_framework.change_mode(t200_play_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            game_framework.change_mode(t400_play_mode)