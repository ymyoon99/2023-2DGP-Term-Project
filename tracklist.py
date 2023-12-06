# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1, SDLK_2
from pico2d import get_events, load_image, clear_canvas, update_canvas, load_wav

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import title_mode
import ready_mode_t200
import ready_mode_t400



def init():
    global image
    global clicksound

    image = load_image('./background/tracklist.jpg')

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


def handle_events(tracklist=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            clicksound.play()
            game_framework.change_mode(title_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            game_framework.change_mode(ready_mode_t200)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            game_framework.change_mode(ready_mode_t400)
