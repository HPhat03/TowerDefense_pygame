from configparser import ConfigParser


config = ConfigParser()
config.read('setting.ini')

DEFAULT = {
    "FPS": 60,
    "MAP_TILE_SIZE": 64,
    "MAP_WIDTH_TILE": 15,
    "MAP_HEIGHT_TILE": 10
}

# MAP SETTING
MAP_TILE_SIZE = config.getint(
    section="map",
    option="MAP_TILE_SIZE",
    fallback=DEFAULT["MAP_TILE_SIZE"]
)
MAP_WIDTH_TILE = config.getint(
    section="map",
    option="MAP_WIDTH_TILE",
    fallback=DEFAULT["MAP_WIDTH_TILE"]
)
MAP_HEIGHT_TILE = config.getint(
    section="map",
    option="MAP_HEIGHT_TILE",
    fallback=DEFAULT["MAP_HEIGHT_TILE"]
)

# WINDOWS SETTING
FPS = config.getint(
    section="window",
    option="FPS",
    fallback=DEFAULT["FPS"]
)
RIGHT_BAR = 300
BOT_BAR = 130
WINDOW_WIDTH = MAP_WIDTH_TILE * MAP_TILE_SIZE + RIGHT_BAR
WINDOW_HEIGHT = MAP_HEIGHT_TILE * MAP_TILE_SIZE + BOT_BAR

# OTHER SETING
DEFAULT_SIZE = 32
button_color = (42, 186, 103)
spawn_cooldown = 1500
