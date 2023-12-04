# External_Library
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import title_mode


def init():
    global image
    global logo_start_time

    image = load_image('./background/loading.png')
    logo_start_time = get_time()


def finish():
    pass


def update():
    global running
    global logo_start_time
    if get_time() - logo_start_time >= 1.0:
        game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    update_canvas()


def handle_events():
    events = get_events()
