from src import db


class Tower:
    def __init__(self, id: int | tuple):
        data = db.select("select * from Tower where id=?", (id, ))

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

    @staticmethod
    def get_all():
        return [{
            "id": data[0],
            "name": data[1],
            "img_src": data[2],
            "in_shop_price": data[3],
            "in_game_price": data[4]
        } for data in db.select("select * from Tower")]
