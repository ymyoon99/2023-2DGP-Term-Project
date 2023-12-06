# External_Library
from pico2d import open_canvas, close_canvas

# Internal_Library
import game_framework
from server_const import *

# Choice_Mode
import logo_mode as release
import t200_play_mode as test

# Programmed for 60 Fps
open_canvas(CANVAS_WEIGHT, CANVAS_HEIGHT, 60)
game_framework.run(release)
close_canvas()
