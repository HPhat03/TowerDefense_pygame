from src.utils.database import Database

db = Database()
l = db.select("select * from Player where name = ?", ("QuyThanh", ))
print(len(l))