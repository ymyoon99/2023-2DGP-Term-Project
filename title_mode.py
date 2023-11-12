from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time

import play_mode


def init():
    global image

    image = load_image('./resource/title.jpg')

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    image.draw(640, 360)
    update_canvas()
    pass

def handle_events(title_mode=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(play_mode)