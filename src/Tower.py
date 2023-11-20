from pygame.sprite import Sprite

from src import db


class Tower(Sprite):
    def __init__(self, id: int | tuple):
        Sprite.__init__(self)
        data = db.select("select * from Tower where id=?", (id, ))[0]

        self.id, self.name, self.img_src, \
            self.in_shop_price, self.in_game_price = data

    def __dict__(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_src": self.img_src,
            "in_shop_price": self.in_shop_price,
            "in_game_price": self.in_game_price
        }

    def __eq__(self, other):
        if not isinstance(other, Tower):
            return NotImplemented

        return self.id == other.id


    @staticmethod
    def get_all():
        return [{
            "id": data[0],
            "name": data[1],
            "img_src": data[2],
            "in_shop_price": data[3],
            "in_game_price": data[4]
        } for data in db.select("select * from Tower")]
