# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
from pico2d import get_events, load_image, clear_canvas, update_canvas, load_wav

# Internal_Library
import game_framework
import server
from server_const import *

import title_mode


def init():
    global image
    global clicksound

    image = load_image('./background/guide.png')
    clicksound = load_wav('./resource/sound/changemenu.wav')
    clicksound.set_volume(32)

def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    update_canvas()
    pass


def handle_events(leaderboard=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            clicksound.play()
            game_framework.change_mode(title_mode)
