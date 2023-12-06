# External_Library
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, load_music

# Internal_Library
import game_framework
from server_const import *

# Linked_Mode
import t200_play_mode
import logo_mode


def init():
    global image
    global mode_start_time
    global countdown

    logo_mode.menubgm.stop()

    image = load_image('./background/ready.png')
    mode_start_time = get_time()

    countdown = load_music('./resource/sound/countdown.mp3')
    countdown.set_volume(32)
    countdown.play(1)


def finish():
    pass


def update():
    global running
    global mode_start_time

    if get_time() - mode_start_time >= 2:
        game_framework.change_mode(t200_play_mode)


def draw():
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    update_canvas()


def handle_events():
    events = get_events()
