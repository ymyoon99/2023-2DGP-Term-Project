# External_Library
from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time

# Internal_Library
import game_framework
import t200_play_mode
from server_const import *

# Linked_Mode
import title_mode


def init():
    global image
    global image2
    global mode_start_time
    global frame, action

    image = load_image('./background/ready.png')
    mode_start_time = get_time()

    image2 = load_image('./resource/firework.png')

    frame = 0
    action = 0


def finish():
    pass


def update():
    global running
    global mode_start_time
    global frame, action


    if get_time() - mode_start_time >= 3.0:
        game_framework.change_mode(t200_play_mode)

    frame = (frame + 1) % 6
    action = (action + 1) % 5


def draw():
    global frame, action
    clear_canvas()
    image.draw(CANVAS_CENTER_X, CANVAS_CENTER_Y)
    # image2.clip_draw(int(frame) * 125, (4 - action) * 505, 125, 505, 100, 100)
    update_canvas()


def handle_events():
    events = get_events()
