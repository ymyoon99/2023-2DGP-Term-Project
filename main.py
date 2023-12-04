# External_Library
import pyglet
from pico2d import open_canvas, close_canvas

# Internal_Library
import game_framework
from server_const import *

# Choice_Mode
import logo_mode as release
import t200_play_mode as test
import lose_mode


open_canvas(CANVAS_WEIGHT, CANVAS_HEIGHT, 60)
game_framework.run(release)
close_canvas()
