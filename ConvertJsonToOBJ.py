class Game:
    def __init(self, title, price, source):
        self.title = title
        self.price = price
        self.source = source

    def get_title(self):
        return self.title

    def get_price(self):
        return self.price

    def get_source(self):
        return self.source
class JsonToGame:

    file = open("games.json")
    x = file.readlines()
    for entry in x:
        x.
    print(x[1])