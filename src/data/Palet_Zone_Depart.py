class Palet_Zone_Depart:

    def __init__(self, zone, color):
        self.zone = zone
        self.color = color

    def to_json(self):
        return {"zone": self.zone, "color": self.color}

    def __str__(self):
        return "zone:%s color:%s" % (self.zone, self.color)