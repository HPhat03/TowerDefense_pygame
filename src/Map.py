import pygame as pg
import json


class Map(pg.sprite.Sprite):
    def __init__(self, map):
        pg.sprite.Sprite.__init__(self)
        self.name = map[1]
        self.img_path = map[2]
        self.image = pg.image.load(self.img_path)
        self.data_path = map[3]
        self.path = map[4]
        self.map_data = []
        self.DataGetting()

    def DataGetting(self):
        self.waypoints = []
        with open(self.data_path) as file:
            map_data = json.load(file)
        for data in map_data["layers"]:
            if data["name"] == "Main":
                self.map_data = data["data"]
                # self.pathBlock = data["path"]
            if data["name"] == "WayPoints":
                for o in data["objects"]:
                    dx = o.get("x")
                    dy = o.get("y")
                    if o["polyline"]:
                        for p in o["polyline"]:
                            x = p.get("x") + dx
                            y = p.get("y") + dy
                            self.waypoints.append((x,y))

    def load(self, surface):
        surface.blit(self.image, (0,0))
        # pg.draw.lines(surface,"black",False,self.waypoints,2)

