# import random
# import math
# import game_framework
#
# from pico2d import *

# class Zombie:
#
#     def load_images(self):
#         if Zombie.images == None:
#             Zombie.images = {}
#             for name in animation_names:
#                 Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]
#
#     def __init__(self):
#         self.x, self.y = random.randint(1600-800, 1600), 150
#         self.load_images()
#
#
#     def update(self):
#         pass
#
#
#     def draw(self):
#
#         if self.dir < 0:
#             Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 200, 200)
#         else:
#             Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 200, 200)
#         draw_rectangle(*self.get_bb())
#
#
#     def handle_event(self, event):
#         pass
#
#     def get_bb(self):
#         return self.x - 70, self.y - 50, self.x + 70, self.y + 50
#
#     def handle_collision(self, group, other):
#         if group == 'ball:zombie':
#             pass
#         if group == 'boy:zombie':
#             game_framework.quit()
#
