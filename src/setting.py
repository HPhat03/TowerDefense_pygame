import pygame
from configparser import ConfigParser

pygame.font.init()
config = ConfigParser()
config.read('setting.ini')

# MAP SETTING
MAP_WIDTH_TILE = 15
MAP_HEIGHT_TILE = 10
MAP_TILE_SIZE = 64

# WINDOWS SETTING
WINDOW_WIDTH= MAP_WIDTH_TILE*MAP_TILE_SIZE
WINDOW_HEIGHT=MAP_HEIGHT_TILE*MAP_TILE_SIZE
FPS = 60

# OTHER SETING
FONT = pygame.font.Font("src/fonts/Baloo2.ttf", 32)
button_color = (42, 186, 103)
