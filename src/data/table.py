from data.palet import Palet


class Table:

    def __init__(self):
        self.purple_chaos = [Palet(0, 0, 'red'), Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'blue')]
        self.yellow_chaos = [Palet(0, 0, 'red'), Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'blue')]
        self.purple_dispenser = [Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'red'), Palet(0, 0, 'blue'),
                                 Palet(0, 0, 'red'), Palet(0, 0, 'green'), ]
        self.yellow_dispenser = [Palet(0, 0, 'green'), Palet(0, 0, 'red'), Palet(0, 0, 'blue'), Palet(0, 0, 'red'),
                                 Palet(0, 0, 'green'), Palet(0, 0, 'red'), ]

    def to_json(self):
        return {"purple_chaos": [palet.to_json() for palet in self.purple_chaos],
                "yellow_chaos": [palet.to_json() for palet in self.purple_chaos],
                "purple_dispenser": [palet.to_json() for palet in self.purple_chaos],
                "yellow_dispenser": [palet.to_json() for palet in self.purple_chaos]
                }
