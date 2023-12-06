# External_Library
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_music

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import title_mode

global menubgm

def init():
    global image
    global logo_start_time
    global menubgm

    image = load_image('./background/loading.png')
    logo_start_time = get_time()

    menubgm = load_music('./resource/sound/menubgm.mp3')
    menubgm.set_volume(32)

def finish():
    pass


def update():
    global running
    global logo_start_time
    if get_time() - logo_start_time >= 1.0:
        menubgm.repeat_play()
        game_framework.change_mode(title_mode)


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    update_canvas()


def handle_events():
    events = get_events()
