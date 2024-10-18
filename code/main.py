import pygame, sys
from settings import *
from level import Level
from level_data import level_0
import pymixer

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SUPER MARIO 2000")
clock = pygame.time.Clock()
level = Level(level_0, screen)
pygame.mixer.music.load("../music/main_theme.ogg")
pygame.mixer.music.play(0, 0.0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("lightblue")
    level.run()

    pygame.display.update()
    clock.tick(60)
