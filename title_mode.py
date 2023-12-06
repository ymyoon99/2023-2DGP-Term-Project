# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDLK_1, SDLK_2, SDLK_3
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_music, load_wav

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import tracklist
import leaderboard
import keyguide


def init():
    global image
    global clicksound

    image = load_image('./background/title.png')

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


def handle_events(title_mode=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            clicksound.play()
            game_framework.change_mode(tracklist)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            clicksound.play()
            game_framework.change_mode(leaderboard)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            clicksound.play()
            game_framework.change_mode(keyguide)
