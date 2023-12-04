# External_Library
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE
from pico2d import get_events, load_image, clear_canvas, update_canvas, load_font

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import title_mode


def init():
    global image
    global font

    image = load_image('./background/lose.jpg')
    font = load_font('./resource/Game.TTF', 40)

def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    font.draw(815, 250, f'AI WON THE GAME', (0, 0, 0))
    update_canvas()
    pass


def handle_events(tracklist=None):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
