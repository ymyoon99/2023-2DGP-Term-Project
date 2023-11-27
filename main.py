# External_Library
from pico2d import open_canvas, delay, close_canvas

# Internal_Library
import game_framework
from server_const import *

# Choice_Mode
import logo_mode as release
import t200_play_mode as start_mode


open_canvas(CANVAS_WEIGHT, CANVAS_HEIGHT)
game_framework.run(release)
close_canvas()

