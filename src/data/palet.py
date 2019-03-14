class Palet:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def to_json(self):
        return {"x": self.x, "y": self.y, "color": self.color}

    def __str__(self):
        return "x:%s y:%s color:%s" % (self.x, self.y, self.color)
