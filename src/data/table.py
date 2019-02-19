from src.data.palet import Palet


class table:

    def __init__(self):
        self.purple_chaos = [Palet(0, 0, 'red'), Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'blue')]
        self.yellow_chaos = [Palet(0, 0, 'red'), Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'blue')]
        self.purple_dispenser = [Palet(0, 0, 'red'), Palet(0, 0, 'green'), Palet(0, 0, 'red'), Palet(0, 0, 'blue'),
                                 Palet(0, 0, 'red'), Palet(0, 0, 'green'), ]
        self.yellow_dispenser = [Palet(0, 0, 'green'), Palet(0, 0, 'red'), Palet(0, 0, 'blue'), Palet(0, 0, 'red'),
                                 Palet(0, 0, 'green'), Palet(0, 0, 'red'), ]
